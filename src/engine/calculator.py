import numpy as np
import pandas as pd
import re

# --- HELPER FUNCTIONS (Kept your existing parsing logic) ---

def safe_int(val, default=0):
    try:
        if pd.isna(val) or val == '': return default
        s_val = str(val)
        match = re.search(r'-?\d+', s_val)
        if match: return int(match.group())
        return default
    except (ValueError, TypeError):
        return default

def parse_d6_value(val):
    if pd.isna(val) or val == '': return 0.0
    val = str(val).upper().strip()
    if 'D' not in val:
        try: return float(val)
        except ValueError: return 0.0
    try:
        if '+' in val:
            parts = val.split('+')
            dice_part = parts[0]
            flat_part = float(parts[1])
        else:
            dice_part = val
            flat_part = 0.0
        
        if dice_part == 'D6': num_dice = 1
        elif dice_part.endswith('D6'): num_dice = float(dice_part.replace('D6', ''))
        else: num_dice = 0
        return (num_dice * 3.5) + flat_part
    except Exception:
        return 0.0

# --- CORE MATH ENGINE ---

def resolve_single_row(row, defender):
    """
    Calculates damage for a single row (one weapon profile).
    Returns a dict with 'dead_models' and 'total_damage'.
    """
    # 1. Parse Attacker Stats from the Series (row)
    attacks = parse_d6_value(row.get('A', 0))
    damage = parse_d6_value(row.get('D', 1))
    bs = safe_int(row.get('BS', 4), default=4)
    s = safe_int(row.get('S', 4), default=4)
    ap = safe_int(row.get('AP', 0), default=0)
    
    sustained_val = safe_int(row.get('Sustained', 0))
    lethal = str(row.get('Lethal', 'N')).upper() == 'Y'
    dev = str(row.get('Dev', 'N')).upper() == 'Y'
    crit_hit_thresh = safe_int(row.get('CritHit', 6), default=6)
    crit_wound_thresh = safe_int(row.get('CritWound', 6), default=6)

    # 2. Hit Phase
    p_crit_hit = max(0, (7 - crit_hit_thresh) / 6.0)
    p_hit_standard = max(0, (7 - bs) / 6.0)
    
    hits = attacks * p_hit_standard
    auto_wounds = 0
    
    if lethal:
        auto_wounds = attacks * p_crit_hit
        hits = max(0, hits - auto_wounds)

    if sustained_val > 0:
        hits += (attacks * p_crit_hit * sustained_val)

    # 3. Wound Phase
    t = safe_int(defender.get('T', 4), default=4)
    if s >= 2 * t: w_roll = 2
    elif s > t:    w_roll = 3
    elif s == t:   w_roll = 4
    elif s > t/2:  w_roll = 5
    else:          w_roll = 6
    
    p_wound_standard = (7 - w_roll) / 6.0
    p_crit_wound = max(0, (7 - crit_wound_thresh) / 6.0)
    p_wound_final = max(p_wound_standard, p_crit_wound)
    
    successful_wounds = hits * p_wound_final
    
    mortal_wounds = 0
    if dev:
        dev_procs = hits * p_crit_wound
        mortal_wounds = dev_procs * damage
        successful_wounds = max(0, successful_wounds - dev_procs)

    successful_wounds += auto_wounds

    # 4. Save Phase
    sv = safe_int(defender.get('Sv'), default=7)
    inv = safe_int(defender.get('Inv'), default=0)
    
    modified_sv = sv - ap
    final_save = modified_sv
    if inv > 0:
        final_save = min(modified_sv, inv)
        
    if final_save > 6: p_fail = 1.0
    else:
        p_save = min((7 - final_save) / 6.0, 5/6.0)
        p_fail = 1.0 - p_save
        
    damage_dealing_wounds = successful_wounds * p_fail

    # 5. Damage Allocation
    model_w = safe_int(defender.get('W', 1), default=1)
    if model_w <= 0: model_w = 1

    damage_per_shot = float(damage)
    kill_efficiency_normal = min(1.0, damage_per_shot / model_w)
    
    dead_from_shots = damage_dealing_wounds * kill_efficiency_normal
    dead_from_mortals = mortal_wounds / model_w
    
    total_dead = dead_from_shots + dead_from_mortals
    total_raw_dmg = (damage_dealing_wounds * damage) + mortal_wounds
    
    return total_dead, total_raw_dmg

# --- MAIN AGGREGATOR ---

def calculate_group_metrics(df, target_profile, deduplicate=True):
    """
    Calculates metrics with "Profile ID" Optimization & Correct Point Scoring.
    """
    if df.empty:
        return []

    # --- 1. PRE-CALCULATE DAMAGE ---
    temp_df = df.copy()
    
    # Sanitize
    if 'Qty' not in temp_df.columns: temp_df['Qty'] = 1
    temp_df['Qty'] = pd.to_numeric(temp_df['Qty'], errors='coerce').fillna(1)
    
    if 'Profile ID' not in temp_df.columns: temp_df['Profile ID'] = ''
    temp_df['Profile ID'] = temp_df['Profile ID'].astype(str).replace('nan', '')

    # Run Math
    metrics = temp_df.apply(lambda row: resolve_single_row(row, target_profile), axis=1, result_type='expand')
    temp_df['row_kills'] = metrics[0]
    temp_df['row_damage'] = metrics[1]
    
    # --- 2. RESOLUTION PHASE (Optimization) ---
    mask_exclusive = temp_df['Profile ID'] != ''
    df_cumulative = temp_df[~mask_exclusive].copy()
    df_exclusive = temp_df[mask_exclusive].copy()
    
    if not df_exclusive.empty:
        # Sort by Kills (primary) then Damage (secondary)
        df_exclusive = df_exclusive.sort_values(
            by=['row_kills', 'row_damage'], 
            ascending=[False, False]
        )
        # Identify Winners
        winners = df_exclusive.drop_duplicates(subset=['Name', 'Pts', 'Profile ID'])
        winning_keys = set(zip(winners['Name'], winners['Pts'], winners['Profile ID'], winners['Weapon']))
        
        # Filter
        df_exclusive_resolved = df_exclusive[
            df_exclusive.apply(lambda x: (x['Name'], x['Pts'], x['Profile ID'], x['Weapon']) in winning_keys, axis=1)
        ]
    else:
        df_exclusive_resolved = pd.DataFrame()

    # Recombine
    work_df = pd.concat([df_cumulative, df_exclusive_resolved], ignore_index=True)

    # --- 3. AGGREGATION PHASE (The Fix) ---

    # Calculate Totals
    # Note: We do NOT multiply Pts here yet. We handle points aggregation separately below.
    if not deduplicate:
        work_df['final_kills'] = work_df['row_kills'] * work_df['Qty']
        work_df['final_damage'] = work_df['row_damage'] * work_df['Qty']
    else:
        work_df['final_kills'] = work_df['row_kills']
        work_df['final_damage'] = work_df['row_damage']

    # Deduplication (Table View)
    if deduplicate:
        subset_cols = ['Name', 'Weapon', 'A', 'BS', 'S', 'AP', 'D', 'Pts', 'Keywords', 'Loadout Group']
        valid_subset = [c for c in subset_cols if c in work_df.columns]
        work_df = work_df.drop_duplicates(subset=valid_subset)

    # Grouping Config
    group_cols = ['Name', 'Loadout Group']
    if 'Qty' in work_df.columns and not deduplicate:
         group_cols.append('Qty')
    
    valid_group_cols = [c for c in group_cols if c in work_df.columns]
    
    # --- POINTS AGGREGATION FIX ---
    # We aggregate Pts using 'max' to avoid double-counting multi-profile units.
    # e.g. Karnivore (Strike) 140pts + Karnivore (Sweep) 140pts -> MAX is 140pts.
    
    agg_funcs = {
        'final_kills': 'sum', 
        'final_damage': 'sum',
        'Pts': 'max',  # <--- CRITICAL FIX: Take MAX cost of the rows in this unit
        'Weapon': lambda x: ", ".join(sorted(set(
            work_df.loc[x.index, 'Weapon'][work_df.loc[x.index, 'Profile ID'] != '']
        )))
    }
    
    grouped = work_df.groupby(valid_group_cols).agg(agg_funcs).reset_index()

    results = []
    target_pts = target_profile.get('Pts', 1)
    target_size = target_profile.get('UnitSize', 10)

    for _, row in grouped.iterrows():
        # Cost Calculation
        unit_cost = float(row['Pts'])
        qty = row.get('Qty', 1) if not deduplicate else 1
        
        # Total Cost = Unit Cost * Qty
        # (Since we used 'max' above, unit_cost is the cost of ONE model)
        total_cost_basis = unit_cost * qty
        
        total_kills = row['final_kills']
        total_dmg = row['final_damage']
        active_modes = row['Weapon']
        
        kv_points = total_kills * target_pts
        
        # CPK = Total Points Spent / Total Points Killed
        cpk = total_cost_basis / kv_points if kv_points > 0 else 999.0 
        ttk = target_size / total_kills if total_kills > 0 else 999.0

        results.append({
            'Unit': row['Name'],
            'Group': row.get('Loadout Group', 'Standard'),
            'Qty': qty,
            'CPK': cpk,
            'Kills': total_kills,
            'TTK': ttk,
            'Damage': total_dmg,
            'Mode': active_modes
        })

    return results
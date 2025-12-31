import numpy as np
import pandas as pd
import re
from .grading import get_cpk_grade

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

def apply_blast_modifier(attack_string, unit_size, has_blast):
    """
    Applies Blast keyword modifier to attack characteristic.

    Blast Rules:
    - 5 or fewer models: No change
    - 6-10 models: Use minimum value (e.g., D6 = 6, 2D6 = 2)
    - 11+ models: Use maximum value (e.g., D6 = 6, D6+3 = 9, 2D6 = 12)

    Args:
        attack_string: Original attack characteristic (e.g., 'D6', '2D6+3', '4')
        unit_size: Number of models in target unit
        has_blast: Whether weapon has Blast keyword

    Returns:
        Modified attack value as string
    """
    if not has_blast or unit_size <= 5:
        return attack_string

    attack_str = str(attack_string).upper().strip()

    # Fixed attacks (no dice) - no change
    if 'D' not in attack_str:
        return attack_string

    # Parse the attack characteristic
    try:
        flat_part = 0
        if '+' in attack_str:
            parts = attack_str.split('+')
            dice_part = parts[0]
            flat_part = int(parts[1])
        else:
            dice_part = attack_str

        # Determine number of dice
        if dice_part == 'D6':
            num_dice = 1
        elif dice_part.endswith('D6'):
            num_dice = int(dice_part.replace('D6', ''))
        else:
            num_dice = 0

        # Apply Blast modifier
        if unit_size >= 11:
            # Maximum: each D6 = 6
            max_value = (num_dice * 6) + flat_part
            return str(max_value)
        elif unit_size >= 6:
            # Minimum: each D6 = 1, but total attacks = num_dice (not num_dice * 1)
            # Actually, "minimum" means the lowest possible roll, which is num_dice
            min_value = num_dice + flat_part
            return str(min_value)
        else:
            return attack_string

    except Exception:
        # If parsing fails, return original
        return attack_string

# --- CORE MATH ENGINE ---

def resolve_single_row(row, defender):
    """
    Calculates damage for a single row (one weapon profile).
    Returns a dict with 'dead_models' and 'total_damage'.
    """
    # 1. Parse Attacker Stats from the Series (row)
    # Apply Blast modifier BEFORE parsing attacks
    blast = str(row.get('Blast', 'N')).upper() == 'Y'
    unit_size = safe_int(defender.get('UnitSize', 10), default=10)
    attack_value = apply_blast_modifier(row.get('A', 0), unit_size, blast)

    attacks = parse_d6_value(attack_value)
    damage = parse_d6_value(row.get('D', 1))
    bs = safe_int(row.get('BS', 4), default=4)
    s = safe_int(row.get('S', 4), default=4)
    ap = safe_int(row.get('AP', 0), default=0)

    sustained_val = safe_int(row.get('Sustained', 0))
    lethal = str(row.get('Lethal', 'N')).upper() == 'Y'
    dev = str(row.get('Dev', 'N')).upper() == 'Y'
    torrent = str(row.get('Torrent', 'N')).upper() == 'Y'
    twin_linked = str(row.get('TwinLinked', 'N')).upper() == 'Y'
    crit_hit_thresh = safe_int(row.get('CritHit', 6), default=6)
    crit_wound_thresh = safe_int(row.get('CritWound', 6), default=6)

    # 2. Hit Phase
    p_crit_hit = max(0, (7 - crit_hit_thresh) / 6.0)

    # Torrent = Auto-hit (ignores BS)
    if torrent:
        p_hit_standard = 1.0  # All attacks hit
        hits = attacks
    else:
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

    p_wound_base = (7 - w_roll) / 6.0
    p_crit_wound = max(0, (7 - crit_wound_thresh) / 6.0)

    # Twin-Linked = Reroll wound rolls (treat as reroll all failures)
    if twin_linked:
        p_wound_with_reroll = p_wound_base + ((1 - p_wound_base) * p_wound_base)
        p_wound_final = max(p_wound_with_reroll, p_crit_wound)
    else:
        p_wound_final = max(p_wound_base, p_crit_wound)

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

    # 5. Feel No Pain (FNP) - Apply to all damage-dealing wounds
    fnp_val = defender.get('FNP', '')
    if fnp_val and fnp_val != '':
        fnp_save = safe_int(fnp_val, default=7)
        if fnp_save <= 6:
            p_fnp_fail = (7 - fnp_save) / 6.0
            # FNP reduces damage-dealing wounds
            damage_dealing_wounds = damage_dealing_wounds * p_fnp_fail
            # Mortal wounds also affected by FNP
            mortal_wounds = mortal_wounds * p_fnp_fail

    # 6. Damage Allocation
    model_w = safe_int(defender.get('W', 1), default=1)
    if model_w <= 0: model_w = 1

    damage_per_shot = float(damage)
    kill_efficiency_normal = min(1.0, damage_per_shot / model_w)

    dead_from_shots = damage_dealing_wounds * kill_efficiency_normal
    dead_from_mortals = mortal_wounds / model_w

    total_dead = dead_from_shots + dead_from_mortals
    total_raw_dmg = (damage_dealing_wounds * damage) + mortal_wounds

    return total_dead, total_raw_dmg

def resolve_weapon_profile(attacker, defender):
    """
    Wrapper function for MCP server compatibility.
    Takes attacker dict and defender dict, returns results dict.

    Args:
        attacker: Dict with keys like 'Pts', 'A', 'BS', 'S', 'AP', 'D',
                  'Sustained', 'Lethal', 'Dev', 'RR_H', 'RR_W'
        defender: Target profile dict from targets.py

    Returns:
        Dict with 'dead_models' and 'total_damage'
    """
    # Convert attacker dict to a pandas Series to match resolve_single_row expectations
    import pandas as pd
    attacker_series = pd.Series(attacker)

    # Call the core calculator
    dead_models, total_damage = resolve_single_row(attacker_series, defender)

    # Return as dict for MCP server
    return {
        'dead_models': dead_models,
        'total_damage': total_damage
    }

# --- MAIN AGGREGATOR ---

def calculate_group_metrics(df, target_profile, deduplicate=True, assume_half_range=False):
    """
    Calculates metrics with "Profile ID" Optimization & Correct Point Scoring.

    Parameters:
    - df: DataFrame with weapon data
    - target_profile: Target stats dict
    - deduplicate: Whether to apply Profile ID optimization (default True)
    - assume_half_range: If True, only use close-range variants for Melta/Rapid Fire (default False)
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

    # --- RANGE-DEPENDENT WEAPONS (Melta, Rapid Fire) ---
    # Duplicate rows for weapons with range-dependent rules
    range_variants = []
    rows_to_remove = []

    for idx, row in temp_df.iterrows():
        has_melta = str(row.get('Melta', 'N')).upper() == 'Y'
        has_rapid_fire = str(row.get('RapidFire', 'N')).upper() == 'Y'

        if has_melta or has_rapid_fire:
            # Preserve user's Profile ID if they set one, otherwise use 'Range'
            # This ensures range variants compete with user-defined modes (e.g., Flamer vs Melta)
            original_profile_id = row.get('Profile ID', '')
            if not original_profile_id or original_profile_id == '':
                profile_id_to_use = 'Range'
            else:
                profile_id_to_use = original_profile_id

            # If assume_half_range is enabled, only create close variant
            if not assume_half_range:
                # Create FAR variant (no bonuses)
                far_row = row.copy()
                far_row['Weapon'] = f"{row['Weapon']} (far)"
                far_row['Profile ID'] = profile_id_to_use
                range_variants.append(far_row)

            # Create CLOSE variant (with bonuses)
            close_row = row.copy()
            if assume_half_range:
                # Don't add suffix if we're assuming half range globally
                close_row['Weapon'] = row['Weapon']
            else:
                close_row['Weapon'] = f"{row['Weapon']} (close)"
            close_row['Profile ID'] = profile_id_to_use

            # Apply Rapid Fire bonus: Double attacks
            if has_rapid_fire:
                current_attacks = str(close_row.get('A', '1'))
                # Double the attack value
                if 'D6' in current_attacks.upper():
                    # Handle dice notation
                    if '+' in current_attacks:
                        parts = current_attacks.split('+')
                        dice_part = parts[0].upper()
                        flat = int(parts[1])
                        if dice_part == 'D6':
                            close_row['A'] = f'2D6+{flat * 2}'
                        elif dice_part.endswith('D6'):
                            num = int(dice_part.replace('D6', ''))
                            close_row['A'] = f'{num * 2}D6+{flat * 2}'
                    else:
                        if current_attacks.upper() == 'D6':
                            close_row['A'] = '2D6'
                        elif current_attacks.upper().endswith('D6'):
                            num = int(current_attacks.upper().replace('D6', ''))
                            close_row['A'] = f'{num * 2}D6'
                else:
                    # Fixed attacks - just double
                    try:
                        attacks = int(current_attacks)
                        close_row['A'] = str(attacks * 2)
                    except:
                        close_row['A'] = current_attacks

            # Apply Melta bonus: Re-roll damage (approximate as +50% damage)
            # Actually, Melta adds +D6 damage at half range
            if has_melta:
                current_damage = str(close_row.get('D', '1'))
                # Add +D6 to damage
                if 'D6' in current_damage.upper():
                    if '+' in current_damage:
                        parts = current_damage.split('+')
                        dice_part = parts[0].upper()
                        flat = int(parts[1])
                        if dice_part == 'D6':
                            close_row['D'] = f'2D6+{flat}'
                        elif dice_part.endswith('D6'):
                            num = int(dice_part.replace('D6', ''))
                            close_row['D'] = f'{num + 1}D6+{flat}'
                    else:
                        if current_damage.upper() == 'D6':
                            close_row['D'] = '2D6'
                        elif current_damage.upper().endswith('D6'):
                            num = int(current_damage.upper().replace('D6', ''))
                            close_row['D'] = f'{num + 1}D6'
                else:
                    # Fixed damage - add 3.5 average
                    try:
                        dmg = int(current_damage)
                        close_row['D'] = f'{dmg}+D6'
                    except:
                        close_row['D'] = current_damage

            range_variants.append(close_row)
            rows_to_remove.append(idx)

    # Remove original rows that were split
    if rows_to_remove:
        temp_df = temp_df.drop(rows_to_remove)

    # Add range variants
    if range_variants:
        temp_df = pd.concat([temp_df, pd.DataFrame(range_variants)], ignore_index=True)

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

        # Get letter grade for CPK
        grade = get_cpk_grade(cpk)

        results.append({
            'Unit': row['Name'],
            'Group': row.get('Loadout Group', 'Standard'),
            'Qty': qty,
            'CPK': cpk,
            'Grade': grade,  # Add letter grade
            'Kills': total_kills,
            'TTK': ttk,
            'Damage': total_dmg,
            'Mode': active_modes
        })

    return results
# src/engine/calculator.py
from .math_core import parse_dice, get_crit_prob, get_hit_prob, calculate_capped_damage

def resolve_weapon_profile(weapon, defender):
    """
    Calculates the raw output of a SINGLE weapon profile.
    Handles Hit -> Wound -> Save -> FNP -> Damage Wastage.
    """
    # 1. Parse Keywords
    sus_val = int(weapon.get('Sustained', 0) or 0)
    is_lethal = str(weapon.get('Lethal', 'N')).upper() == 'Y'
    is_dev = str(weapon.get('Dev', 'N')).upper() == 'Y'
    crit_h = int(weapon.get('CritHit', 6) or 6)
    crit_w = int(weapon.get('CritWound', 6) or 6)

    # 2. Hit Sequence
    bs = int(str(weapon['BS']).replace('+', ''))
    rr_h = str(weapon.get('RR_H', 'N')).upper()
    
    p_hit_total = get_hit_prob(bs, rr_h)
    actual_crit_h = max(crit_h, bs)
    p_crit_h = get_crit_prob(actual_crit_h, rr_h)
    p_hit_norm = max(0, p_hit_total - p_crit_h)

    # Hit Triggers
    attacks = int(weapon['A'])
    bonus_hits = attacks * p_crit_h * sus_val
    auto_wounds = attacks * p_crit_h if is_lethal else 0
    hits_to_wound = (attacks * p_hit_norm) + (0 if is_lethal else attacks * p_crit_h) + bonus_hits

    # 3. Wound Sequence
    s, t = int(weapon['S']), int(defender['T'])
    if s >= 2*t: req=2
    elif s > t: req=3
    elif s == t: req=4
    elif s <= t/2: req=6
    else: req=5
    
    req = min(req, crit_w) # Anti-X override
    rr_w = str(weapon.get('RR_W', 'N')).upper()
    
    p_w_raw = (7 - req) / 6.0
    if rr_w == '1': p_w_total = p_w_raw + (1/6.0 * p_w_raw)
    elif rr_w == 'F': p_w_total = p_w_raw + ((1 - p_w_raw) * p_w_raw)
    else: p_w_total = p_w_raw
    
    p_crit_w = get_crit_prob(crit_w, rr_w)
    p_w_norm = max(0, p_w_total - p_crit_w)

    # 4. Save Sequence
    sv = int(str(defender['Sv']).replace('+', ''))
    ap = abs(int(weapon['AP']))
    inv = int(str(defender['Inv']).replace('+', '')) if defender['Inv'] else 99
    
    save_roll = min(sv + ap, inv)
    p_fail = 1.0 if save_roll > 6 else 1.0 - ((7 - save_roll)/6.0)

    # 5. Damage Sequence
    succ_norm_w = hits_to_wound * p_w_norm
    succ_crit_w = hits_to_wound * p_crit_w
    
    mortals = succ_crit_w if is_dev else 0
    saves_to_roll = succ_norm_w + auto_wounds + (0 if is_dev else succ_crit_w)
    
    unsaved = saves_to_roll * p_fail
    
    # --- FNP (FEEL NO PAIN) LOGIC ---
    fnp_str = str(defender.get('FNP', '')).replace('+', '')
    if fnp_str and fnp_str.isdigit():
        fnp_val = int(fnp_str)
        p_fail_fnp = (fnp_val - 1) / 6.0
    else:
        p_fail_fnp = 1.0 # 100% chance to take damage (no FNP)
    
    # Effective Wounds logic handles FNP + Wastage interaction best for averages
    raw_wounds = int(defender['W'])
    effective_wounds = raw_wounds / p_fail_fnp
    
    # Total Damage Events (Failed Saves + Mortals)
    # Note: Mortals also get FNP (usually), unless specified otherwise. Assuming standard FNP.
    total_dmg_events = unsaved + mortals
    
    # Calculate Average Damage per Event (Capped by Effective Wounds)
    dmg_prof = parse_dice(weapon['D'])
    avg_dmg = calculate_capped_damage(dmg_prof, effective_wounds)
    
    total_damage_dealt = total_dmg_events * avg_dmg
    dead_models = total_damage_dealt / effective_wounds
    
    return {
        'dead_models': dead_models
    }

def calculate_group_metrics(roster_df, defender_profile):
    """
    Aggregation Engine:
    1. Group rows by 'Name' and 'Loadout Group'.
    2. Sum the dead models.
    3. Cap at Unit Size.
    """
    metrics = []
    
    # Ensure Loadout Group exists
    if 'Loadout Group' not in roster_df.columns:
        roster_df['Loadout Group'] = 'Default'
    
    # Fill NaN
    roster_df['Loadout Group'] = roster_df['Loadout Group'].fillna('Default')

    grouped = roster_df.groupby(['Name', 'Loadout Group'])
    
    for (unit_name, group_name), group_df in grouped:
        
        total_dead = 0
        total_pts = group_df['Pts'].iloc[0] # Assume points match across group
        
        for _, row in group_df.iterrows():
            res = resolve_weapon_profile(row, defender_profile)
            total_dead += res['dead_models']
            
        # --- UNIT SIZE CAP ---
        unit_cap = defender_profile.get('UnitSize', 99)
        final_kills = min(total_dead, unit_cap)
        
        # Metrics
        if final_kills > 0:
            cpk = total_pts / (final_kills * defender_profile['Pts'])
            ttk = 1.0 / final_kills
        else:
            cpk = 99.9
            ttk = 99.9
            
        metrics.append({
            'Unit': unit_name,
            'Group': group_name,
            'Target': defender_profile['Name'],
            'CPK': round(cpk, 2),
            'Kills': round(final_kills, 2),
            'TTK': round(ttk, 2)
        })
        
    return metrics
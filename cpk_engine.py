import math

def parse_dice(dice_str):
    """
    Parses 'D6+1', '3', '2D6'. Returns dict for calculation.
    """
    dice_str = str(dice_str).upper().strip()
    if 'D' not in dice_str:
        return {'count': 0, 'faces': 0, 'modifier': float(dice_str), 'is_fixed': True}
    
    parts = dice_str.split('+')
    dice_part = parts[0]
    mod = int(parts[1]) if len(parts) > 1 else 0
    
    count = 1
    faces = 6
    if 'D3' in dice_part:
        faces = 3
        if dice_part != 'D3': count = int(dice_part.replace('D3',''))
    elif 'D6' in dice_part:
        faces = 6
        if dice_part != 'D6': count = int(dice_part.replace('D6',''))
            
    return {'count': count, 'faces': faces, 'modifier': mod, 'is_fixed': False}

def get_crit_prob(thresh, rr_type):
    p = (7 - thresh) / 6.0
    if rr_type == '1': return p + (1/6.0 * p)
    if rr_type == 'F': return p + ((1 - ((thresh - 1)/6.0)) * p)
    return p

def calculate_capped_damage(damage_profile, target_wounds):
    if damage_profile['is_fixed']:
        return min(damage_profile['modifier'], target_wounds)
    
    count = damage_profile['count']
    faces = damage_profile['faces']
    mod = damage_profile['modifier']
    
    total = 0
    iters = 0
    if count == 1:
        for r in range(1, faces+1):
            total += min(r + mod, target_wounds)
            iters += 1
        return total / iters
    elif count == 2:
        for r1 in range(1, faces+1):
            for r2 in range(1, faces+1):
                total += min(r1 + r2 + mod, target_wounds)
                iters += 1
        return total / iters
    else:
        avg = (count * (faces + 1) / 2) + mod
        return min(avg, target_wounds)

def calculate_cpk(attacker, defender):
    """
    The Core Logic. 
    Accepts two dictionaries: attacker (stats) and defender (target profile).
    Returns a float (CPK).
    """
    # Setup keywords (defaulting to safe values if missing)
    sus_val = int(attacker.get('Sustained', 0) or 0)
    
    # Handle 'Y'/'N' or boolean inputs for flags
    def parse_bool(val):
        return str(val).upper() == 'Y' or val is True

    is_lethal = parse_bool(attacker.get('Lethal', 'N'))
    is_dev = parse_bool(attacker.get('Dev', 'N'))
    
    crit_h = int(attacker.get('CritHit', 6) or 6)
    crit_w = int(attacker.get('CritWound', 6) or 6)

    # 1. Hit Logic
    bs = int(str(attacker['BS']).replace('+', ''))
    rr_h = str(attacker.get('RR_H', 'N')).upper()
    
    # Crit Hit Probability
    actual_crit_h = max(crit_h, bs)
    p_crit_h = get_crit_prob(actual_crit_h, rr_h)
    
    # Normal Hit Probability
    p_hit_base = (7 - bs) / 6.0
    if rr_h == '1': p_hit_total = p_hit_base + (1/6.0 * p_hit_base)
    elif rr_h == 'F': p_hit_total = p_hit_base + ((1 - p_hit_base) * p_hit_base)
    else: p_hit_total = p_hit_base
    
    p_hit_norm = max(0, p_hit_total - p_crit_h)

    # 2. Hit Effects (Sustained / Lethal)
    attacks = int(attacker['A'])
    bonus = attacks * p_crit_h * sus_val
    auto_w = attacks * p_crit_h if is_lethal else 0
    hits_to_wound = (attacks * p_hit_norm) + (0 if is_lethal else attacks * p_crit_h) + bonus

    # 3. Wound Logic
    s, t = int(attacker['S']), int(defender['T'])
    if s >= 2*t: req=2
    elif s > t: req=3
    elif s == t: req=4
    elif s <= t/2: req=6
    else: req=5
    
    # Anti-X overrides standard wound chart
    req = min(req, crit_w)
    
    rr_w = str(attacker.get('RR_W', 'N')).upper()
    p_crit_w = get_crit_prob(crit_w, rr_w)
    
    p_w_base = (7 - req) / 6.0
    if rr_w == '1': p_w_total = p_w_base + (1/6.0 * p_w_base)
    elif rr_w == 'F': p_w_total = p_w_base + ((1 - p_w_base) * p_w_base)
    else: p_w_total = p_w_base
    
    p_w_norm = max(0, p_w_total - p_crit_w)

    # 4. Saves
    sv = int(str(defender['Sv']).replace('+', ''))
    ap = abs(int(attacker['AP']))
    inv = int(str(defender['Inv']).replace('+', '')) if defender['Inv'] else 99
    
    save_roll = min(sv + ap, inv)
    p_fail = 1.0 if save_roll > 6 else 1.0 - ((7 - save_roll)/6.0)

    # 5. Damage & Wastage
    succ_norm_w = hits_to_wound * p_w_norm
    succ_crit_w = hits_to_wound * p_crit_w
    
    mortals = succ_crit_w if is_dev else 0
    saves_to_roll = succ_norm_w + auto_w + (0 if is_dev else succ_crit_w)
    
    unsaved = saves_to_roll * p_fail
    total_dmg_events = unsaved + mortals
    
    dmg_prof = parse_dice(attacker['D'])
    target_w = int(defender['W'])
    avg_dmg = calculate_capped_damage(dmg_prof, target_w)
    
    dead = (total_dmg_events * avg_dmg) / target_w
    
    if dead <= 0: return 999.9
    
    cpk = int(attacker['Pts']) / (dead * int(defender['Pts']))
    return round(cpk, 2)

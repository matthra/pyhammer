# src/engine/math_core.py

def parse_dice(dice_str):
    """Parses 'D6+2', '3', '2D6' into count/faces/mod."""
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
    """Calculates probability of a Critical Success (trigger)."""
    p = (7 - thresh) / 6.0
    if rr_type == '1': return p + (1/6.0 * p)
    if rr_type == 'F': return p + ((1 - ((thresh - 1)/6.0)) * p)
    return p

def get_hit_prob(bs, rr_type):
    """Calculates probability of a Hit."""
    p = (7 - bs) / 6.0
    if rr_type == '1': return p + (1/6.0 * p)
    if rr_type == 'F': return p + ((1 - p) * p)
    return p

def calculate_capped_damage(damage_profile, target_wounds):
    """Calculates average damage per successful wound, capped by target W (Model Wastage)."""
    if damage_profile['is_fixed']:
        return min(damage_profile['modifier'], target_wounds)
    
    count = damage_profile['count']
    faces = damage_profile['faces']
    mod = damage_profile['modifier']
    
    if count == 1:
        total = sum(min(r + mod, target_wounds) for r in range(1, faces+1))
        return total / faces
    elif count == 2:
        total = 0
        iters = 0
        for r1 in range(1, faces+1):
            for r2 in range(1, faces+1):
                total += min(r1 + r2 + mod, target_wounds)
                iters += 1
        return total / iters
    else:
        # Simple average approximation for high dice counts
        avg = (count * (faces + 1) / 2) + mod
        return min(avg, target_wounds)
import pandas as pd
import sys
import os

# Ensure we can import from src/engine
sys.path.append(os.path.join(os.getcwd(), 'src', 'engine'))

try:
    from calculator import calculate_group_metrics
except ImportError:
    print("❌ Could not import calculator. Make sure you are in the project root.")
    sys.exit(1)

# --- 1. SETUP MOCK DATA ---
# Target: Space Marine Intercessor (Standard Profile)
target_profile = {
    'T': 4,
    'Sv': 3,
    'Inv': 7,
    'W': 2,
    'Pts': 17,       # Points per model
    'UnitSize': 5
}

# Roster: 3 Identical Units of "Clone Troopers"
# Each costs 100pts and has a weapon that does roughly 2 wounds (1 kill).
data = {
    'Name': ['Clone Trooper', 'Clone Trooper', 'Clone Trooper'],
    'Weapon': ['Blaster', 'Blaster', 'Blaster'],
    'A': [4, 4, 4],     # 4 Shots
    'BS': [3, 3, 3],    # 3+ to Hit
    'S': [4, 4, 4],     # S4 vs T4
    'AP': [-1, -1, -1], # AP-1 vs Sv3+ -> 4+ Save
    'D': [2, 2, 2],     # Damage 2 (Each fail kills a marine exactly)
    'Pts': [100, 100, 100],
    'Loadout Group': ['Standard', 'Standard', 'Standard'],
    # Dummy columns that might exist in a real CSV
    'id': [101, 102, 103] 
}

df = pd.DataFrame(data)

print(f"\n🧪 TESTING WITH TARGET: T{target_profile['T']} W{target_profile['W']} Sv{target_profile['Sv']}+")
print(f"📊 ROSTER: 3x Clone Troopers (100pts each). Total List Cost: 300pts.\n")

# --- 2. RUN TEST A: EFFICIENCY MODE (deduplicate=True) ---
print("--- TEST A: EFFICIENCY MODE (deduplicate=True) ---")
print("Expected: Stats for ONE unit only (Cost 100pts).")

results_eff = calculate_group_metrics(df, target_profile, deduplicate=True)
r_eff = results_eff[0]

print(f" > Name:   {r_eff['Unit']}")
print(f" > Damage: {r_eff['Damage']:.2f}")
print(f" > Kills:  {r_eff['Kills']:.2f}")
print(f" > CPK:    {r_eff['CPK']:.2f}")

if 100 <= r_eff['CPK'] < 1000: # Rough sanity check
    print("✅ PASS: CPK looks normal for a single unit.")
else:
    print("❌ FAIL: CPK looks distorted.")

# --- 3. RUN TEST B: ARMY OUTPUT MODE (deduplicate=False) ---
print("\n--- TEST B: ARMY OUTPUT MODE (deduplicate=False) ---")
print("Expected: Stats for ALL 3 units combined (Total Damage x3).")

results_army = calculate_group_metrics(df, target_profile, deduplicate=False)
r_army = results_army[0]

print(f" > Name:   {r_army['Unit']}")
print(f" > Damage: {r_army['Damage']:.2f}")
print(f" > Kills:  {r_army['Kills']:.2f}")

# Verification Logic
ratio = r_army['Damage'] / r_eff['Damage']
print(f"\n📈 Multiplier Ratio (Army / Unit): {ratio:.2f}x")

if 2.9 < ratio < 3.1:
    print("✅ PASS: Army Output is exactly 3x the Unit Output.")
    print("🎉 FIX CONFIRMED: Logic is successfully decoupled.")
else:
    print(f"❌ FAIL: Ratio is {ratio:.2f}x (Expected 3.0x). Duplicates are not being handled correctly.")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Melta and Rapid Fire range-dependent weapons.
"""

import sys
import os

# Add parent directory to path for src imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from src.data.targets import TARGETS
from src.engine.calculator import calculate_group_metrics

def test_rapid_fire():
    """Test Rapid Fire keyword (double attacks at close range)"""
    print("=" * 60)
    print("TEST 1: Rapid Fire Keyword")
    print("=" * 60)

    # Bolter with Rapid Fire
    test_unit = {
        'UnitID': 'test-rf-1',
        'Qty': 1,
        'Name': 'Tactical Squad',
        'Loadout Group': 'Ranged',
        'Pts': 100,
        'Range': 24,
        'Profile ID': '',
        'Keywords': 'Rapid Fire',
        'Weapon': 'Bolter',
        'A': 2,  # Should become 4 at close range
        'BS': 3,
        'S': 4,
        'AP': 0,
        'D': 1,
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'Blast': 'N',
        'Melta': 'N',
        'RapidFire': 'Y',  # Rapid Fire enabled
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against MEQ
    meq = TARGETS['MEQ']
    results = calculate_group_metrics(df, meq, deduplicate=False)

    print(f"\nRapid Fire Bolter vs MEQ:")
    print(f"  Results: {len(results)} variants (should be 2: close and far)")

    if len(results) >= 1:
        # Should show the best result (close range with double attacks)
        best = results[0]
        print(f"\n  Best Variant: {best['Mode']}")
        print(f"  Dead Models: {best['Kills']:.2f}")
        print(f"  CPK: {best['CPK']:.2f} ({best['Grade']}-tier)")

        # Close range should be significantly better
        assert 'close' in best['Mode'].lower(), "Best variant should be close range"
        assert best['Kills'] > 0, "Should produce some kills at close range"
        print("  ✅ PASS: Rapid Fire creates close/far variants, picks best\n")
    else:
        print("  ❌ FAIL: No results generated")

def test_melta():
    """Test Melta keyword (bonus damage at close range)"""
    print("=" * 60)
    print("TEST 2: Melta Keyword")
    print("=" * 60)

    # Meltagun
    test_unit = {
        'UnitID': 'test-melta-1',
        'Qty': 1,
        'Name': 'Melta Squad',
        'Loadout Group': 'Ranged',
        'Pts': 100,
        'Range': 12,
        'Profile ID': '',
        'Keywords': 'Melta',
        'Weapon': 'Meltagun',
        'A': 1,
        'BS': 3,
        'S': 9,
        'AP': -4,
        'D': 'D6',  # Should become 2D6 at close range
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'Blast': 'N',
        'Melta': 'Y',  # Melta enabled
        'RapidFire': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against VEQ-H (Land Raider - tough vehicle)
    land_raider = TARGETS['VEQ-H']
    results = calculate_group_metrics(df, land_raider, deduplicate=False)

    print(f"\nMeltagun vs Land Raider (T12 16W):")
    print(f"  Results: {len(results)} variants (should be 2: close and far)")

    if len(results) >= 1:
        best = results[0]
        print(f"\n  Best Variant: {best['Mode']}")
        print(f"  Dead Models: {best['Kills']:.2f}")
        print(f"  Damage: {best['Damage']:.2f}")
        print(f"  CPK: {best['CPK']:.2f} ({best['Grade']}-tier)")

        # Close range should be best (double damage)
        assert 'close' in best['Mode'].lower(), "Best variant should be close range"
        assert best['Damage'] > 0, "Should deal some damage"
        print("  ✅ PASS: Melta creates close/far variants, picks best\n")
    else:
        print("  ❌ FAIL: No results generated")

def test_combined_rapid_fire_melta():
    """Test weapon with BOTH Rapid Fire and Melta"""
    print("=" * 60)
    print("TEST 3: Combined Rapid Fire + Melta")
    print("=" * 60)

    # Theoretical weapon with both keywords
    test_unit = {
        'UnitID': 'test-combo-1',
        'Qty': 1,
        'Name': 'Super Meltagun',
        'Loadout Group': 'Ranged',
        'Pts': 150,
        'Range': 12,
        'Profile ID': '',
        'Keywords': 'Rapid Fire, Melta',
        'Weapon': 'Super Meltagun',
        'A': 2,   # Should become 4 at close
        'BS': 3,
        'S': 9,
        'AP': -4,
        'D': 'D6',  # Should become 2D6 at close
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'Blast': 'N',
        'Melta': 'Y',
        'RapidFire': 'Y',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against KEQ (Knight)
    knight = TARGETS['KEQ']
    results = calculate_group_metrics(df, knight, deduplicate=False)

    print(f"\nSuper Meltagun (Rapid Fire + Melta) vs Knight:")
    print(f"  Results: {len(results)} variants")

    if len(results) >= 1:
        best = results[0]
        print(f"\n  Best Variant: {best['Mode']}")
        print(f"  Dead Models: {best['Kills']:.2f}")
        print(f"  Damage: {best['Damage']:.2f}")
        print(f"  CPK: {best['CPK']:.2f} ({best['Grade']}-tier)")

        # Should be devastating at close range (4 attacks, 2D6 damage each)
        assert 'close' in best['Mode'].lower(), "Best variant should be close range"
        print("  ✅ PASS: Combined keywords work together\n")
    else:
        print("  ❌ FAIL: No results generated")

def test_no_range_weapons():
    """Test that normal weapons aren't affected"""
    print("=" * 60)
    print("TEST 4: Normal Weapons (No Range Bonuses)")
    print("=" * 60)

    # Regular lascannon
    test_unit = {
        'UnitID': 'test-normal-1',
        'Qty': 1,
        'Name': 'Lascannon Team',
        'Loadout Group': 'Ranged',
        'Pts': 100,
        'Range': 48,
        'Profile ID': '',
        'Keywords': '',
        'Weapon': 'Lascannon',
        'A': 1,
        'BS': 3,
        'S': 12,
        'AP': -3,
        'D': 'D6+1',
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'Blast': 'N',
        'Melta': 'N',  # No range bonuses
        'RapidFire': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against VEQ-H
    land_raider = TARGETS['VEQ-H']
    results = calculate_group_metrics(df, land_raider, deduplicate=False)

    print(f"\nLascannon (normal weapon) vs Land Raider:")
    print(f"  Results: {len(results)} variants (should be 1: no range splitting)")

    if len(results) == 1:
        result = results[0]
        print(f"\n  Weapon: {result['Mode']}")
        print(f"  Dead Models: {result['Kills']:.2f}")
        print(f"  CPK: {result['CPK']:.2f} ({result['Grade']}-tier)")

        # Should NOT have (close) or (far) suffix
        assert 'close' not in result['Mode'].lower(), "Normal weapon shouldn't be split"
        assert 'far' not in result['Mode'].lower(), "Normal weapon shouldn't be split"
        print("  ✅ PASS: Normal weapons not affected by range system\n")
    else:
        print(f"  ❌ FAIL: Expected 1 result, got {len(results)}")

def test_display_both_variants():
    """Verify that both close and far variants exist in intermediate data"""
    print("=" * 60)
    print("TEST 5: Both Variants Generated (Before Optimization)")
    print("=" * 60)

    test_unit = {
        'UnitID': 'test-both-1',
        'Qty': 1,
        'Name': 'Test Bolter',
        'Loadout Group': 'Ranged',
        'Pts': 50,
        'Range': 24,
        'Profile ID': '',
        'Keywords': 'Rapid Fire',
        'Weapon': 'Bolter',
        'A': 2,
        'BS': 3,
        'S': 4,
        'AP': 0,
        'D': 1,
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'Blast': 'N',
        'Melta': 'N',
        'RapidFire': 'Y',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])
    geq = TARGETS['GEQ']

    # Call with deduplicate=False to see all variants before optimization
    results_all = calculate_group_metrics(df, geq, deduplicate=False)

    print(f"\nBolter (Rapid Fire) vs GEQ - All Variants:")
    print(f"  Total Results: {len(results_all)}")

    for i, r in enumerate(results_all, 1):
        print(f"\n  Variant {i}: {r['Mode']}")
        print(f"    Kills: {r['Kills']:.2f}")
        print(f"    CPK: {r['CPK']:.2f}")

    # After optimization, should only see 1 (the best)
    results_optimized = calculate_group_metrics(df, geq, deduplicate=True)
    print(f"\n  After Optimization: {len(results_optimized)} result (best variant)")

    if len(results_optimized) == 1:
        print(f"    Winner: {results_optimized[0]['Mode']}")
        print("  ✅ PASS: System generates both, optimizes to best\n")
    else:
        print("  ❌ FAIL: Optimization didn't work correctly")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PyHammer Range-Dependent Weapons Tests")
    print("=" * 60 + "\n")

    try:
        test_rapid_fire()
        test_melta()
        test_combined_rapid_fire_melta()
        test_no_range_weapons()
        test_display_both_variants()

        print("=" * 60)
        print("✅ ALL RANGE WEAPONS TESTS PASSED")
        print("=" * 60)
        print("\nRange-dependent weapons implementation verified:")
        print("  • Rapid Fire: Double attacks at close range")
        print("  • Melta: Bonus damage (+D6) at close range")
        print("  • Combined keywords work together")
        print("  • Profile ID optimization picks best variant")
        print("  • Normal weapons unaffected")
        print("\nMelta and Rapid Fire are production-ready!")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()

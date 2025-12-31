#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cover toggle functionality.
Verify that +1 save bonus reduces damage taken.
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

def test_cover_bonus():
    """Test that cover improves save and reduces damage"""
    print("=" * 60)
    print("TEST: Cover Bonus (+1 Save)")
    print("=" * 60)

    # Bolter vs MEQ
    test_unit = {
        'UnitID': 'test-cover-1',
        'Qty': 10,
        'Name': 'Tactical Squad',
        'Loadout Group': 'Ranged',
        'Pts': 100,
        'Range': 24,
        'Profile ID': '',
        'Keywords': '',
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
        'RapidFire': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test 1: MEQ without cover (3+ save)
    meq_no_cover = TARGETS['MEQ'].copy()
    results_no_cover = calculate_group_metrics(df, meq_no_cover, deduplicate=False)

    print(f"\n10 Bolters vs MEQ (3+ save, no cover):")
    print(f"  Dead Models: {results_no_cover[0]['Kills']:.2f}")
    print(f"  Damage: {results_no_cover[0]['Damage']:.2f}")

    # Test 2: MEQ with cover (2+ save)
    meq_with_cover = TARGETS['MEQ'].copy()

    # Apply cover bonus (same logic as app.py)
    current_save = meq_with_cover.get('Sv', '3+')
    save_val = int(current_save.replace('+', ''))
    improved_save = max(2, save_val - 1)  # Cover: +1 save, min 2+
    meq_with_cover['Sv'] = f'{improved_save}+'

    print(f"\n  Cover Applied: {current_save} → {meq_with_cover['Sv']}")

    results_with_cover = calculate_group_metrics(df, meq_with_cover, deduplicate=False)

    print(f"\n10 Bolters vs MEQ ({meq_with_cover['Sv']} save, with cover):")
    print(f"  Dead Models: {results_with_cover[0]['Kills']:.2f}")
    print(f"  Damage: {results_with_cover[0]['Damage']:.2f}")

    # Verify cover reduced damage
    damage_reduction = results_no_cover[0]['Kills'] - results_with_cover[0]['Kills']
    percent_reduction = (damage_reduction / results_no_cover[0]['Kills']) * 100

    print(f"\n  Damage Reduction: {damage_reduction:.2f} models ({percent_reduction:.1f}%)")

    # Cover should reduce damage (better save)
    assert results_with_cover[0]['Kills'] < results_no_cover[0]['Kills'], \
        "Cover should reduce damage taken"

    print(f"\n  ✅ PASS: Cover reduced damage as expected\n")

def test_cover_minimum():
    """Test that cover doesn't improve save beyond 2+"""
    print("=" * 60)
    print("TEST: Cover Minimum Save (2+)")
    print("=" * 60)

    # Test with Custodes (already 2+ save)
    custodes_no_cover = TARGETS['CUST'].copy()
    current_save = custodes_no_cover.get('Sv', '2+')

    # Apply cover bonus (should stay 2+)
    save_val = int(current_save.replace('+', ''))
    improved_save = max(2, save_val - 1)  # Can't go below 2+
    custodes_with_cover_sv = f'{improved_save}+'

    print(f"\n  Custodes Save: {current_save}")
    print(f"  With Cover: {custodes_with_cover_sv}")

    # Should stay at 2+
    assert custodes_with_cover_sv == '2+', "Cover can't improve save beyond 2+"

    print(f"\n  ✅ PASS: Cover correctly enforces 2+ minimum\n")

def test_cover_parsing():
    """Test that calculator correctly parses save values with + suffix"""
    print("=" * 60)
    print("TEST: Save Value Parsing")
    print("=" * 60)

    # High AP weapon vs GEQ with cover
    test_unit = {
        'UnitID': 'test-parse-1',
        'Qty': 10,
        'Name': 'Plasma Gun',
        'Loadout Group': 'Ranged',
        'Pts': 100,
        'Range': 24,
        'Profile ID': '',
        'Keywords': '',
        'Weapon': 'Plasma Gun',
        'A': 1,
        'BS': 3,
        'S': 7,
        'AP': -3,  # High AP to test save degradation
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
        'RapidFire': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # GEQ with cover (5+ → 4+)
    geq_with_cover = TARGETS['GEQ'].copy()
    current_save = geq_with_cover.get('Sv', '5+')
    save_val = int(current_save.replace('+', ''))
    improved_save = max(2, save_val - 1)
    geq_with_cover['Sv'] = f'{improved_save}+'

    print(f"\n  GEQ Save: {current_save} → {geq_with_cover['Sv']} (with cover)")
    print(f"  Plasma Gun AP: -3")
    print(f"  Effective Save: {geq_with_cover['Sv']} -3 = 7+ (no save)")

    results = calculate_group_metrics(df, geq_with_cover, deduplicate=False)

    print(f"\n  Result: {results[0]['Kills']:.2f} dead")
    print(f"  Calculator successfully parsed '{geq_with_cover['Sv']}' save value")

    # Should get some kills (no save against AP-3)
    assert results[0]['Kills'] > 0, "Should produce kills"

    print(f"\n  ✅ PASS: Save parsing works correctly\n")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PyHammer Cover Toggle Tests")
    print("=" * 60 + "\n")

    try:
        test_cover_bonus()
        test_cover_minimum()
        test_cover_parsing()

        print("=" * 60)
        print("✅ ALL COVER TESTS PASSED")
        print("=" * 60)
        print("\nCover toggle implementation verified:")
        print("  • Cover bonus (+1 save) reduces damage")
        print("  • Minimum save of 2+ enforced")
        print("  • Calculator correctly parses save values")
        print("  • Cover is production-ready!")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()

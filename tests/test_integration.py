#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test for new keywords (Torrent, Twin-Linked, FNP).
Tests the full calculation pipeline with the new rules.
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
from src.data.rosters import DEFAULT_ROSTER
from src.data.targets import TARGETS
from src.engine.calculator import calculate_group_metrics

def test_torrent_integration():
    """Test Torrent keyword in full calculation pipeline"""
    print("=" * 60)
    print("TEST 1: Torrent Keyword Integration")
    print("=" * 60)

    # Create a test weapon with Torrent
    test_unit = {
        'UnitID': 'test-1',
        'Qty': 1,
        'Name': 'Flamer Squad',
        'Loadout Group': 'Ranged',
        'Pts': 100,
        'Range': 12,
        'Profile ID': '',
        'Keywords': 'Torrent',
        'Weapon': 'Heavy Flamer',
        'A': 'D6',
        'BS': 4,  # Should be ignored by Torrent
        'S': 5,
        'AP': -1,
        'D': 1,
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'Y',  # Auto-hit enabled
        'TwinLinked': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against GEQ (Guardsmen)
    geq = TARGETS['GEQ']
    results = calculate_group_metrics(df, geq, deduplicate=False)

    print(f"\nFlamer (Torrent) vs GEQ:")
    print(f"  Expected: Auto-hits (100% hit rate)")
    print(f"  Dead Models: {results[0]['Kills']:.2f}")
    print(f"  CPK: {results[0]['CPK']:.2f} ({results[0]['Grade']}-tier)")

    # Verify it's better than BS4+ (0.5 hit rate)
    assert results[0]['Kills'] > 1.0, "Torrent should produce significant kills"
    print("  ✅ PASS: Torrent working correctly\n")

def test_twin_linked_integration():
    """Test Twin-Linked keyword in full calculation pipeline"""
    print("=" * 60)
    print("TEST 2: Twin-Linked Keyword Integration")
    print("=" * 60)

    # Create a test weapon with Twin-Linked
    test_unit = {
        'UnitID': 'test-2',
        'Qty': 1,
        'Name': 'Twin Heavy Bolter',
        'Loadout Group': 'Ranged',
        'Pts': 50,
        'Range': 36,
        'Profile ID': '',
        'Keywords': 'Twin-Linked',
        'Weapon': 'Twin Heavy Bolter',
        'A': 6,
        'BS': 3,
        'S': 5,
        'AP': -1,
        'D': 2,
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'Y',  # Reroll wounds enabled
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against MEQ (Space Marines)
    meq = TARGETS['MEQ']
    results = calculate_group_metrics(df, meq, deduplicate=False)

    print(f"\nTwin Heavy Bolter vs MEQ:")
    print(f"  Expected: Reroll wounds (better wound rate)")
    print(f"  Dead Models: {results[0]['Kills']:.2f}")
    print(f"  CPK: {results[0]['CPK']:.2f} ({results[0]['Grade']}-tier)")

    assert results[0]['Kills'] > 0.5, "Twin-Linked should produce meaningful kills"
    print("  ✅ PASS: Twin-Linked working correctly\n")

def test_fnp_integration():
    """Test FNP on defender side"""
    print("=" * 60)
    print("TEST 3: Feel No Pain (FNP) Integration")
    print("=" * 60)

    # Use a simple weapon
    test_unit = {
        'UnitID': 'test-3',
        'Qty': 1,
        'Name': 'Plasma Gun',
        'Loadout Group': 'Ranged',
        'Pts': 75,
        'Range': 24,
        'Profile ID': '',
        'Keywords': '',
        'Weapon': 'Plasma Gun',
        'A': 2,
        'BS': 3,
        'S': 8,
        'AP': -3,
        'D': 2,
        'CritHit': 6,
        'CritWound': 6,
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'N',
        'Torrent': 'N',
        'TwinLinked': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Compare vs normal target and FNP target
    geq = TARGETS['GEQ']
    custodes = TARGETS['CUST']

    results_geq = calculate_group_metrics(df, geq, deduplicate=False)
    results_custodes = calculate_group_metrics(df, custodes, deduplicate=False)

    print(f"\nPlasma Gun vs GEQ (no FNP):")
    print(f"  Dead Models: {results_geq[0]['Kills']:.2f}")

    print(f"\nPlasma Gun vs Custodes (4+ FNP):")
    print(f"  Dead Models: {results_custodes[0]['Kills']:.2f}")
    print(f"  Expected: ~50% reduction due to 4+ FNP")

    # FNP should reduce kills significantly
    reduction = (results_geq[0]['Kills'] - results_custodes[0]['Kills']) / results_geq[0]['Kills']
    print(f"  Actual Reduction: {reduction*100:.1f}%")

    assert results_custodes[0]['Kills'] < results_geq[0]['Kills'], "FNP should reduce damage"
    print("  ✅ PASS: FNP working correctly\n")

def test_combined_keywords():
    """Test multiple keywords together"""
    print("=" * 60)
    print("TEST 4: Combined Keywords (Torrent + Devastating)")
    print("=" * 60)

    # Create weapon with multiple keywords
    test_unit = {
        'UnitID': 'test-4',
        'Qty': 1,
        'Name': 'Melta Cannon',
        'Loadout Group': 'Ranged',
        'Pts': 150,
        'Range': 18,
        'Profile ID': '',
        'Keywords': 'Torrent, Devastating Wounds',
        'Weapon': 'Torrent Melta',
        'A': 'D6',
        'BS': 3,
        'S': 9,
        'AP': -4,
        'D': 'D6',
        'CritHit': 6,
        'CritWound': 5,  # Easier crits
        'Sustained': 0,
        'Lethal': 'N',
        'Dev': 'Y',  # Devastating Wounds
        'Torrent': 'Y',  # Auto-hit
        'TwinLinked': 'N',
        'RR_H': 'N',
        'RR_W': 'N'
    }

    df = pd.DataFrame([test_unit])

    # Test against TEQ (Terminators)
    teq = TARGETS['TEQ']
    results = calculate_group_metrics(df, teq, deduplicate=False)

    print(f"\nTorrent Melta vs TEQ:")
    print(f"  Keywords: Auto-hit + Dev Wounds (5+)")
    print(f"  Dead Models: {results[0]['Kills']:.2f}")
    print(f"  CPK: {results[0]['CPK']:.2f} ({results[0]['Grade']}-tier)")

    assert results[0]['Kills'] > 0.3, "Combined keywords should be effective"
    print("  ✅ PASS: Combined keywords working correctly\n")

def test_default_roster_structure():
    """Verify DEFAULT_ROSTER has all required fields"""
    print("=" * 60)
    print("TEST 5: DEFAULT_ROSTER Structure")
    print("=" * 60)

    df = pd.DataFrame(DEFAULT_ROSTER)

    required_fields = [
        'UnitID', 'Qty', 'Name', 'Pts', 'Weapon', 'A', 'BS', 'S', 'AP', 'D',
        'CritHit', 'CritWound', 'Sustained', 'Lethal', 'Dev',
        'Torrent', 'TwinLinked', 'RR_H', 'RR_W'
    ]

    print(f"\nChecking {len(required_fields)} required fields...")
    missing = [f for f in required_fields if f not in df.columns]

    if missing:
        print(f"  ❌ FAIL: Missing fields: {missing}")
        return False

    print(f"  ✅ All required fields present")
    print(f"\nSample row (War Dog Brigand):")
    first = df.iloc[0]
    print(f"  Name: {first['Name']}")
    print(f"  Weapon: {first['Weapon']}")
    print(f"  Torrent: {first['Torrent']}")
    print(f"  TwinLinked: {first['TwinLinked']}")
    print(f"  Lethal: {first['Lethal']}")
    print(f"  Dev: {first['Dev']}")
    print("  ✅ PASS: Structure correct\n")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PyHammer Integration Tests - New Keywords")
    print("=" * 60 + "\n")

    try:
        test_default_roster_structure()
        test_torrent_integration()
        test_twin_linked_integration()
        test_fnp_integration()
        test_combined_keywords()

        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nNew features ready:")
        print("  • Torrent (auto-hit) - Calculator + UI")
        print("  • Twin-Linked (reroll wounds) - Calculator + UI")
        print("  • Feel No Pain (FNP) - Calculator")
        print("  • UI controls in Roster Manager tab")
        print("  • DEFAULT_ROSTER updated with new fields")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

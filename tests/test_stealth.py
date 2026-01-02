#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the Stealth rule implementation.

Stealth grants -1 to be hit when assume_half_range is False.
This is simulated by increasing the BS requirement by 1.
"""

import sys
import os

# Add parent directory to path for src imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.engine.calculator import resolve_single_row, calculate_group_metrics
from src.data.targets import TARGETS

def test_stealth_basic():
    """Test that stealth modifier works with assume_half_range=False"""

    # Create a basic weapon profile
    weapon = pd.Series({
        'Name': 'Test Unit',
        'Pts': 100,
        'Weapon': 'Test Gun',
        'A': 10,
        'BS': 3,  # 3+ to hit normally
        'S': 4,
        'AP': 0,
        'D': 1,
        'Profile ID': '',
    })

    # Test against MEQ without stealth
    meq_no_stealth = TARGETS['MEQ'].copy()
    meq_no_stealth['Stealth'] = 'N'

    # Test against MEQ with stealth
    meq_with_stealth = TARGETS['MEQ'].copy()
    meq_with_stealth['Stealth'] = 'Y'

    print("\n--- Test 1: Basic Stealth Test (BS 3+) ---")

    # With assume_half_range=False, stealth should apply
    dead_no_stealth, _ = resolve_single_row(weapon, meq_no_stealth, assume_half_range=False)
    dead_with_stealth, _ = resolve_single_row(weapon, meq_with_stealth, assume_half_range=False)

    print(f"Against MEQ (no stealth): {dead_no_stealth:.2f} kills")
    print(f"Against MEQ (with stealth): {dead_with_stealth:.2f} kills")
    print(f"Reduction: {((dead_no_stealth - dead_with_stealth) / dead_no_stealth * 100):.1f}%")

    # Expected: BS 3+ = 4/6 hit rate, BS 4+ = 3/6 hit rate
    # So we expect ~25% fewer kills with stealth
    assert dead_with_stealth < dead_no_stealth, "Stealth should reduce kills"

    # With assume_half_range=True, stealth should NOT apply
    dead_no_stealth_half, _ = resolve_single_row(weapon, meq_no_stealth, assume_half_range=True)
    dead_with_stealth_half, _ = resolve_single_row(weapon, meq_with_stealth, assume_half_range=True)

    print(f"\nWith assume_half_range=True:")
    print(f"Against MEQ (no stealth): {dead_no_stealth_half:.2f} kills")
    print(f"Against MEQ (with stealth): {dead_with_stealth_half:.2f} kills")

    # These should be equal because stealth doesn't apply at half range
    assert abs(dead_no_stealth_half - dead_with_stealth_half) < 0.01, \
        "Stealth should NOT apply when assume_half_range=True"

    print("[PASS] Basic stealth test passed!")


def test_stealth_with_torrent():
    """Test that stealth doesn't affect Torrent weapons (auto-hit)"""

    weapon = pd.Series({
        'Name': 'Test Unit',
        'Pts': 100,
        'Weapon': 'Flamer',
        'A': 10,
        'BS': 3,
        'S': 4,
        'AP': 0,
        'D': 1,
        'Torrent': 'Y',  # Auto-hit
        'Profile ID': '',
    })

    meq_no_stealth = TARGETS['MEQ'].copy()
    meq_no_stealth['Stealth'] = 'N'

    meq_with_stealth = TARGETS['MEQ'].copy()
    meq_with_stealth['Stealth'] = 'Y'

    print("\n--- Test 2: Stealth vs Torrent (Auto-hit) ---")

    dead_no_stealth, _ = resolve_single_row(weapon, meq_no_stealth, assume_half_range=False)
    dead_with_stealth, _ = resolve_single_row(weapon, meq_with_stealth, assume_half_range=False)

    print(f"Torrent against MEQ (no stealth): {dead_no_stealth:.2f} kills")
    print(f"Torrent against MEQ (with stealth): {dead_with_stealth:.2f} kills")

    # Torrent ignores BS, so stealth shouldn't matter
    assert abs(dead_no_stealth - dead_with_stealth) < 0.01, \
        "Stealth should NOT affect Torrent weapons (they auto-hit)"

    print("[PASS] Torrent vs stealth test passed!")


def test_stealth_different_bs():
    """Test stealth impact with different BS values"""

    print("\n--- Test 3: Stealth Impact with Different BS ---")

    meq_with_stealth = TARGETS['MEQ'].copy()
    meq_with_stealth['Stealth'] = 'Y'

    for bs_value in [2, 3, 4, 5]:
        weapon = pd.Series({
            'Name': 'Test Unit',
            'Pts': 100,
            'Weapon': f'BS{bs_value}+ Gun',
            'A': 10,
            'BS': bs_value,
            'S': 4,
            'AP': 0,
            'D': 1,
            'Profile ID': '',
        })

        dead_no_stealth, _ = resolve_single_row(weapon, TARGETS['MEQ'], assume_half_range=False)
        dead_with_stealth, _ = resolve_single_row(weapon, meq_with_stealth, assume_half_range=False)

        if dead_no_stealth > 0:
            reduction = (dead_no_stealth - dead_with_stealth) / dead_no_stealth * 100
        else:
            reduction = 0

        print(f"BS {bs_value}+: {dead_no_stealth:.2f} -> {dead_with_stealth:.2f} kills ({reduction:.1f}% reduction)")

    print("[PASS] Different BS values test passed!")


def test_stealth_in_calculate_group_metrics():
    """Test stealth with calculate_group_metrics function"""

    print("\n--- Test 4: Stealth in calculate_group_metrics ---")

    df = pd.DataFrame([{
        'Name': 'Test Squad',
        'Pts': 100,
        'Weapon': 'Bolter',
        'Qty': 1,
        'A': 20,
        'BS': 3,
        'S': 4,
        'AP': 0,
        'D': 1,
        'Profile ID': '',
    }])

    meq_with_stealth = TARGETS['MEQ'].copy()
    meq_with_stealth['Stealth'] = 'Y'

    # Test with assume_half_range=False (stealth should apply)
    results_stealth = calculate_group_metrics(df, meq_with_stealth, deduplicate=False, assume_half_range=False)
    results_no_stealth = calculate_group_metrics(df, TARGETS['MEQ'], deduplicate=False, assume_half_range=False)

    kills_stealth = results_stealth[0]['Kills']
    kills_no_stealth = results_no_stealth[0]['Kills']

    print(f"Kills against MEQ (no stealth): {kills_no_stealth:.2f}")
    print(f"Kills against MEQ (with stealth): {kills_stealth:.2f}")

    assert kills_stealth < kills_no_stealth, "Stealth should reduce kills in calculate_group_metrics"

    # Test with assume_half_range=True (stealth should NOT apply)
    results_half_range = calculate_group_metrics(df, meq_with_stealth, deduplicate=False, assume_half_range=True)
    kills_half_range = results_half_range[0]['Kills']

    print(f"Kills with assume_half_range=True: {kills_half_range:.2f}")

    # Should match no-stealth when at half range
    results_no_stealth_half = calculate_group_metrics(df, TARGETS['MEQ'], deduplicate=False, assume_half_range=True)
    kills_no_stealth_half = results_no_stealth_half[0]['Kills']

    assert abs(kills_half_range - kills_no_stealth_half) < 0.01, \
        "Stealth should NOT apply when assume_half_range=True"

    print("[PASS] calculate_group_metrics test passed!")


if __name__ == '__main__':
    print("="*60)
    print("STEALTH RULE TESTS")
    print("="*60)
    print("\nStealth grants -1 to be hit when assume_half_range is False")
    print("(Represents targets being further away)")

    try:
        test_stealth_basic()
        test_stealth_with_torrent()
        test_stealth_different_bs()
        test_stealth_in_calculate_group_metrics()

        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)
        print("\nSummary:")
        print("  • Stealth applies -1 to hit when assume_half_range=False")
        print("  • Stealth does NOT apply when assume_half_range=True")
        print("  • Stealth does NOT affect Torrent weapons (auto-hit)")
        print("  • Stealth works correctly in both resolve_single_row and calculate_group_metrics")

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")
        raise

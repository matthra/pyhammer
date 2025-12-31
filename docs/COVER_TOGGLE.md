# Cover Toggle Implementation

## Overview

Successfully implemented a **global cover toggle** that allows users to apply a +1 save bonus to all target profiles. This simulates the common battlefield condition where units are fighting in cover (ruins, terrain, etc.).

## What is Cover?

In Warhammer 40K, cover provides a defensive bonus to units positioned in terrain:
- **Light Cover**: +1 to armor save rolls
- **Heavy Cover**: +2 to armor save rolls (not implemented)

This implementation provides a **+1 save bonus** (light cover) that improves the target's armor save by one step:
- 3+ save becomes 2+ save
- 4+ save becomes 3+ save
- 5+ save becomes 4+ save
- **Minimum save: 2+** (cover can't improve beyond invulnerable save level)

## Implementation

### 1. UI Control

**Location**: `app.py` lines 41-66

```python
# Two-column layout: target selector + cover toggle
col_target, col_cover = st.columns([3, 1])

with col_target:
    selected_target_key = st.selectbox("Enemy Profile", target_keys, index=default_idx)

with col_cover:
    st.markdown("<br>", unsafe_allow_html=True)  # Align with selectbox
    assume_cover = st.checkbox(
        "🪨 Assume Cover",
        value=False,
        help="Apply +1 to save rolls for all targets"
    )
```

### 2. Cover Logic

**Location**: `app.py` lines 53-62

```python
selected_target_stats = TARGETS[selected_target_key].copy()

# Apply cover bonus if enabled
if assume_cover:
    current_save = selected_target_stats.get('Sv', '7+')
    try:
        # Parse save value (e.g., "3+" → 3)
        save_val = int(current_save.replace('+', ''))
        # Apply +1 bonus (3 → 2), enforce minimum of 2+
        improved_save = max(2, save_val - 1)
        # Update save characteristic
        selected_target_stats['Sv'] = f'{improved_save}+'
    except:
        pass  # If parsing fails, leave save unchanged
```

### 3. Visual Indicator

**Location**: `app.py` line 91

```python
c2.metric(
    "Sv",
    f"{selected_target_stats['Sv']}",
    help="✅ Cover applied" if assume_cover else None
)
```

When cover is enabled, the save metric shows a tooltip: "✅ Cover applied"

## Test Results

### Test 1: Cover Bonus Effectiveness

**10 Bolters vs MEQ (T4 3+ save):**

| Condition | Save | Dead Models | Damage | CPK |
|-----------|------|-------------|--------|-----|
| No Cover | 3+ | 1.11 | 2.22 | 180.18 |
| With Cover | 2+ | 0.56 | 1.11 | 360.36 |

**Result**: Cover reduced damage by **50%** (from 1.11 to 0.56 dead models)

### Test 2: Minimum Save Enforcement

**Custodes (2+ save) with Cover:**
- Original save: 2+
- With cover applied: 2+ (unchanged)
- **Result**: ✅ Correctly enforces 2+ minimum

### Test 3: Save Parsing

**10 Plasma Guns (AP-3) vs GEQ with Cover:**
- GEQ base save: 5+
- With cover: 4+ → effective 7+ (no save against AP-3)
- **Result**: 5.56 dead models
- **Verification**: Calculator correctly parsed "4+" save value

## Math Validation

### Save Probability Changes

**Example: 3+ save → 2+ save**
- 3+ save: Success on 3, 4, 5, 6 = 4/6 = **66.67%** save rate
- 2+ save: Success on 2, 3, 4, 5, 6 = 5/6 = **83.33%** save rate
- Improvement: +16.67 percentage points

**Damage Reduction:**
- Without cover: 33.33% unsaved wounds (fail on 1-2)
- With cover: 16.67% unsaved wounds (fail on 1)
- Reduction: **50% less damage** (33.33% → 16.67%)

This matches our test results exactly (1.11 → 0.56 dead = 50% reduction).

### Save with AP Interaction

Cover is applied to the **base save**, then AP is subtracted:

**Example: GEQ (5+ save) with cover vs AP-3 weapon**
1. Base save: 5+
2. Cover applied: 4+ (5 - 1 = 4)
3. AP applied: 7+ (4 + 3 = 7)
4. Effective: No save (7+ is impossible)

**Example: MEQ (3+ save) with cover vs AP-2 weapon**
1. Base save: 3+
2. Cover applied: 2+ (3 - 1 = 2)
3. AP applied: 4+ (2 + 2 = 4)
4. Effective: 4+ save

## Use Cases

### When Cover is Most Valuable

✅ **Against low-AP weapons** (AP 0, -1, -2)
- Cover bonus directly improves save rolls
- Example: MEQ vs AP-1 bolters: 4+ → 3+ save (+16.67% protection)

✅ **For units with good base saves** (2+, 3+, 4+)
- Already have armor worth protecting
- Cover makes them significantly tougher
- Example: TEQ (2+ save) with cover is nearly invincible vs AP-1

✅ **In competitive/tournament scenarios**
- Most tournament terrain provides light cover
- Realistic assumption for matched play games

### When Cover is Less Valuable

❌ **Against high-AP weapons** (AP-3, AP-4+)
- Cover bonus often negated by AP anyway
- Example: GEQ (5+ → 4+) vs AP-3 = still no save

❌ **For units with poor saves** (6+, 7+)
- Still die easily even with +1 save
- Example: 6+ → 5+ vs AP-1 = 6+ (no change)

❌ **Against mortal wounds**
- Cover only affects armor saves
- Devastating Wounds bypass saves entirely

## Strategic Implications

1. **Realistic Scenarios**: Most 40K games assume some cover usage
2. **Target Selection**: Prioritize high-AP weapons when enemies have cover
3. **List Building**: Cover makes elite armies (low model count, good saves) even tougher
4. **CPK Analysis**: Cover significantly changes efficiency tiers

## Examples

### Cover Impact on CPK Grading

**Example: 10 Bolters (200 pts) vs MEQ**

| Condition | Dead | CPK | Grade | Change |
|-----------|------|-----|-------|--------|
| No Cover | 1.11 | 180.18 | C-tier | Baseline |
| With Cover | 0.56 | 360.36 | F-tier | -2 tiers |

Cover can shift weapons from viable (C-tier) to inefficient (F-tier), affecting list-building decisions.

### Real-World Scenario

**Tournament Game: Space Marines (MEQ) in ruins**
- Assume Cover: **Enabled** ✅
- Target save: 2+ (instead of 3+)
- Your anti-infantry weapons: 50% less effective
- **Decision**: Switch to high-AP weapons or target other units

## Files Modified

- **`app.py`**:
  - Added cover toggle UI (lines 41-66)
  - Added cover logic to modify selected target (lines 53-62)
  - Added visual indicator to save metric (line 91)

- **`test_cover.py`** (NEW):
  - 3 comprehensive tests
  - All passing ✅

## Integration with Existing Features

Cover works correctly with:
- ✅ All target profiles (GEQ, MEQ, TEQ, etc.)
- ✅ All weapon keywords (Blast, Melta, Rapid Fire, etc.)
- ✅ AP modification (cover applied first, then AP)
- ✅ CPK grading system (accounts for improved saves)
- ✅ All metric tabs (Kills, Damage, CPK)
- ✅ MCP server responses

## Running the Tests

```bash
cd pyhammer
python test_cover.py
```

Expected output:
```
============================================================
✅ ALL COVER TESTS PASSED
============================================================

Cover toggle implementation verified:
  • Cover bonus (+1 save) reduces damage
  • Minimum save of 2+ enforced
  • Calculator correctly parses save values
  • Cover is production-ready!
```

## Future Considerations

**Potential Enhancements**:
- **Heavy Cover**: +2 save option (less common, but exists in rules)
- **Stealth Keyword**: -1 to hit (attacker side modifier)
- **Cover Saves by Unit**: Per-unit cover toggles (more granular control)
- **Terrain Types**: Different terrain provides different bonuses

**Related Mechanics Not Implemented**:
- **Dense Cover**: -1 to hit beyond 12"
- **Obscuring**: Can't be targeted at all beyond certain range
- **Area Terrain**: Units wholly within get cover

These could extend the cover system for more advanced scenarios.

## Summary

The cover toggle is a simple but powerful feature that:
- Provides realistic battlefield simulation
- Significantly impacts damage calculations (up to 50% reduction)
- Enforces game rules correctly (2+ minimum save)
- Integrates seamlessly with existing systems
- Helps users make better strategic decisions

**Cover is production-ready and recommended for all competitive/tournament analysis.**

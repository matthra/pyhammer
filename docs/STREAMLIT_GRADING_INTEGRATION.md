# Streamlit Grading Integration

## Overview

The CPK grading system is now fully integrated into the PyHammer Streamlit dashboard, providing visual color-coded efficiency ratings for all units.

## What Changed

### 1. Import Grading Functions (Line 16)
```python
from src.engine.grading import get_cpk_grade, get_grade_color
```

### 2. Added Grade-Based Styling Function (Line 383-394)
```python
def style_cpk_by_grade(val):
    """
    Returns background color based on CPK grade.
    Maps S-tier (green) to F-tier (red).
    """
    if pd.isna(val) or val >= 999:
        return 'background-color: #9E9E9E'  # Gray for invalid

    grade = get_cpk_grade(val)
    color = get_grade_color(grade)
    return f'background-color: {color}'
```

### 3. Updated CPK Tab (Line 442-481)

**Added Grade Legend:**
- Collapsible expander with visual grade reference
- 7-column layout showing S through F tiers
- Each grade displays: letter, CPK range, color, and description

**Updated Table Styling:**
- Replaced `background_gradient(cmap='RdYlGn_r')` with `applymap(style_cpk_by_grade)`
- Now uses discrete grade-based colors instead of continuous gradient
- S-tier: Gold (#FFD700) → F-tier: Red (#F44336)

## Visual Result

### Grade Legend (Collapsible)
```
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│   S    │   A    │   B    │   C    │   D    │   E    │   F    │
│  ≤1.0  │  ≤1.5  │  ≤2.0  │  ≤2.5  │  ≤3.0  │  ≤3.5  │  >3.5  │
│ Elite  │Excel.  │  Good  │Average │Below   │  Poor  │Ineffec.│
└────────┴────────┴────────┴────────┴────────┴────────┴────────┘
 [Gold]  [Green] [Lt Grn] [Yellow] [Orange] [Dp Org]  [Red]
```

### CPK Table Example
```
Unit                  | GEQ  | MEQ  | TEQ  | CUST | ...
─────────────────────────────────────────────────────
Intercessors [Std]    | 2.10 | 5.00 | 8.20 | 9.50 | ...
                      | [🟡] | [🔴] | [🔴] | [🔴] |
Terminators [Std]     | 1.30 | 2.40 | 3.80 | 5.20 | ...
                      | [🟢] | [🟡] | [🔴] | [🔴] |
Lascannon Squad [Std] | 0.85 | 1.20 | 1.50 | 1.90 | ...
                      | [🟡] | [🟢] | [🟢] | [🟢] |
```

## Color Gradient Explanation

The gradient flows from "best efficiency" (S-tier) to "worst efficiency" (F-tier):

| Grade | Color | Hex Code | Meaning |
|-------|-------|----------|---------|
| S | 🔵 Blue | #2196F3 | Elite - removes similarly costed units in one interaction |
| A | 🟢 Green | #00D084 | Excellent trade efficiency |
| B | 🟢 Light Green | #4CAF50 | Good trade efficiency |
| C | 🟡 Yellow | #FFC107 | Average - roughly neutral trades |
| D | 🟠 Orange | #FF9800 | Below average - unfavorable trades |
| E | 🟠 Deep Orange | #FF5722 | Poor - very unfavorable trades |
| F | 🔴 Red | #F44336 | Ineffective - minimal game impact |

## User Benefits

1. **Instant Visual Feedback**: Users can immediately see which units are efficient vs inefficient against each target
2. **No Mental Math**: Don't need to remember "is 2.3 good or bad?" - just look at the color
3. **Quick Comparison**: Easy to scan the table and find S/A-tier units for specific matchups
4. **Educational**: Grade legend teaches users what CPK values mean in practice

## Technical Notes

- Uses Pandas `style.applymap()` to apply per-cell styling
- Styling function is pure (no side effects), making it cacheable
- Handles edge cases: NaN values and ineffective units (CPK ≥ 999) get gray color
- Legend uses Streamlit's `st.expander()` to keep UI clean when not needed

## Future Enhancements (Optional)

1. **Add grade column**: Show letter grade alongside CPK value (e.g., "1.70 (B)")
2. **Grade filter**: Allow filtering table to show only S/A tier units
3. **Grade statistics**: Show distribution of grades across the army
4. **Tooltips**: Hover to see full grade description

## Testing

To verify the integration works:
```bash
streamlit run app.py
```

Navigate to the "💰 Efficiency (CPK)" tab and verify:
- ✓ Grade legend appears in collapsible expander
- ✓ Table cells are colored by grade
- ✓ Colors match the S→F gradient (gold to red)
- ✓ No console errors or warnings

# Kills Tab Upgrade: CPK-Based Color Coding

## Overview

The Lethality (Kills) tab now uses CPK-based grade coloring instead of an arbitrary gradient, providing meaningful visual feedback about unit efficiency.

## Problem

**Before:** The Kills tab used a simple gradient (0-5 kills) that colored cells based on raw kill count:
- Green = high kill count
- Red = low kill count

**Issue:** This doesn't tell you if the unit is *efficient*. A unit might kill many models but be point-inefficient, or kill few models but be extremely cost-effective.

## Solution

**After:** Cells are now colored based on the **CPK (efficiency grade)** while displaying **kill count**:
- Blue/Green = efficient killer (good CPK)
- Red = inefficient killer (bad CPK)

This helps identify units that are both lethal AND efficient, versus units that just deal damage without good point trades.

## Technical Implementation

### 1. Enhanced `build_metric_data` Function

Added optional `include_cpk` parameter:

```python
def build_metric_data(metric_key, include_cpk=False):
    """
    Returns TWO or THREE dataframes:
    1. df_values: The numeric stats (CPK, Kills, etc)
    2. df_tooltips: The text to show on hover (Active Profiles)
    3. df_cpk: (Optional) CPK values for styling purposes
    """
```

When `include_cpk=True`, returns an additional dataframe containing CPK values with the same shape/index as the metric data.

### 2. New Helper Function: `get_cpk_background_colors`

```python
def get_cpk_background_colors(df_cpk):
    """
    Converts a dataframe of CPK values into a dataframe of background colors.
    Returns a dataframe with CSS background-color strings.
    """
    def cpk_to_color(val):
        if pd.isna(val) or val >= 999:
            return 'background-color: #9E9E9E'
        grade = get_cpk_grade(val)
        color = get_grade_color(grade)
        return f'background-color: {color}'

    return df_cpk.map(cpk_to_color)
```

This function converts a dataframe of CPK values into CSS styling strings using the same grade-based color scheme as the CPK tab.

### 3. Updated Kills Tab Rendering

```python
with tab_kills:
    st.caption("Higher is Better (Expected Kills per Activation) - Color coded by efficiency grade")

    if not edited_df.empty:
        # Get kills data AND cpk data
        vals, tips, cpk_vals = build_metric_data('Kills', include_cpk=True)

        if not vals.empty:
            # Generate CPK-based color styles
            styles = get_cpk_background_colors(cpk_vals)

            # Display Kills values with CPK colors
            st.dataframe(
                vals.style.apply(lambda _: styles, axis=None)
                          .format("{:.2f}"),
                width='stretch',
                height=500
            )
```

## Example Use Case

### Scenario: Comparing Two Units

**Unit A: "Glass Cannon"**
- Kills: 8.5 models
- CPK: 6.2 (F-tier)
- Cell color: **Red**
- Interpretation: Kills many models, but very inefficient (costs too many points)

**Unit B: "Efficient Killer"**
- Kills: 3.2 models
- CPK: 0.9 (S-tier)
- Cell color: **Blue**
- Interpretation: Kills fewer models, but extremely efficient (great point trade)

### Visual Result

```
Unit         | GEQ  | MEQ  | TEQ  |
─────────────────────────────────────
Unit A       | 8.50 | 5.20 | 2.10 |
(Glass Cannon)│ [🔴] │ [🔴] │ [🔴] │

Unit B       | 3.20 | 1.80 | 0.90 |
(Efficient)  │ [🔵] │ [🟢] │ [🟢] │
```

Now users can instantly identify units that are **both lethal AND efficient** - the holy grail of list building.

## Benefits

1. **Meaningful Colors**: Color now represents efficiency, not just raw output
2. **Better Decisions**: Helps identify point-efficient killers vs. trap units
3. **Consistency**: All metric tabs use the same S-F color grading system
4. **Visual Clarity**: Easy to spot units that deliver good returns on investment

## Pandas Compatibility

Uses `DataFrame.map()` (Pandas 2.1+) with fallback to `applymap()` for older versions:

```python
try:
    return df_cpk.map(cpk_to_color)
except AttributeError:
    return df_cpk.applymap(cpk_to_color)  # Older pandas
```

## Files Modified

- `app.py`:
  - Enhanced `build_metric_data()` with `include_cpk` parameter
  - Added `get_cpk_background_colors()` helper function
  - Updated Kills tab to use CPK-based coloring
  - Updated CPK tab to use `.map()` instead of deprecated `.applymap()`

## Testing

To verify:
1. Run `streamlit run app.py`
2. Navigate to "💀 Lethality (Kills)" tab
3. Verify cells are colored by efficiency grade (not kill count)
4. Compare with CPK tab - colors should match for same units vs same targets

## Future Enhancements (Optional)

1. Add grade legend to Kills tab (like CPK tab)
2. Show CPK value in tooltip on hover
3. Option to toggle between "color by efficiency" vs "color by lethality"

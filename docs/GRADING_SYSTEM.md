# CPK Grading System

## Overview

The CPK (Cost Per Kill) grading system converts raw efficiency metrics into intuitive letter grades (S-F tier), making it easier for users and LLMs to understand unit performance at a glance.

## Philosophy

**Problem**: Lower CPK = better efficiency is counterintuitive (humans expect higher = better)

**Solution**: Map CPK to letter grades where S = best, F = worst

## Grade Scale

Based on game duration analysis (5-turn games, median CPK ~2.5):

| Grade | CPK Range | Meaning | Trade Efficiency |
|-------|-----------|---------|------------------|
| **S** | ≤ 1.0 | Elite | Removes similarly costed units in one interaction |
| **A** | 1.0 - 1.5 | Excellent | Very favorable trades |
| **B** | 1.5 - 2.0 | Good | Favorable trades |
| **C** | 2.0 - 2.5 | Average | Roughly neutral trades (median) |
| **D** | 2.5 - 3.0 | Below average | Unfavorable trades |
| **E** | 3.0 - 3.5 | Poor | Very unfavorable trades |
| **F** | > 3.5 | Ineffective | Minimal game impact |

## Color Scheme

Grades include color codes for visualizations:

- **S-tier**: Blue (#2196F3) - Distinct special tier
- **A-tier**: Green (#00D084)
- **B-tier**: Light Green (#4CAF50)
- **C-tier**: Yellow/Amber (#FFC107)
- **D-tier**: Orange (#FF9800)
- **E-tier**: Deep Orange (#FF5722)
- **F-tier**: Red (#F44336)

## Usage

### In Python Code

```python
from src.engine.grading import get_cpk_grade, get_grade_color, format_cpk_with_grade

# Get grade
cpk = 1.7
grade = get_cpk_grade(cpk)  # Returns: 'B'

# Get color for visualization
color = get_grade_color(grade)  # Returns: '#4CAF50'

# Formatted output
formatted = format_cpk_with_grade(cpk, include_description=True)
# Returns: "1.70 (B-tier: Good efficiency)"
```

### In MCP Server

The MCP server automatically includes grades in responses:

```
**VS Marines (T4 2W)**
- Dead Models: 1.23
- CPK: 1.70 (B-tier)
- Efficiency: Good efficiency
- Est. Activations to Kill: 0.81
```

### In Streamlit Dashboard

The `calculate_group_metrics()` function now includes a `'Grade'` field in results:

```python
from src.engine.calculator import calculate_group_metrics

results = calculate_group_metrics(df, target_profile)
# Each result now has: {..., 'CPK': 1.7, 'Grade': 'B', ...}
```

### Custom Thresholds

You can override the default thresholds if needed:

```python
custom_thresholds = {
    'S': 0.8,   # Stricter S-tier
    'A': 1.3,
    'B': 1.8,
    'C': 2.3,
    'D': 2.8,
    'E': 3.3,
    'F': None
}

grade = get_cpk_grade(cpk_value, thresholds=custom_thresholds)
```

## Integration Points

1. **MCP Server** (`mcp_server.py`): Includes grade in tool responses for LLMs
2. **Calculator** (`src/engine/calculator.py`): Adds `'Grade'` field to all results
3. **Grading Module** (`src/engine/grading.py`): Centralized grading logic
4. **Visualizations** (future): Use `get_grade_color()` for color-coded charts

## Files Modified

- `src/engine/grading.py` - New grading system module
- `src/engine/calculator.py` - Added grade to results
- `mcp_server.py` - Includes grade in MCP responses
- `example_grading_usage.py` - Integration examples

## Benefits for LLMs

Before:
```
User: "Is a lascannon good against Knights?"
LLM: "The CPK is 1.04, which is... um... lower than average I think?"
```

After:
```
User: "Is a lascannon good against Knights?"
LLM: "Yes! It has A-tier efficiency (CPK 1.04) - excellent trade efficiency."
```

The letter grade makes it trivial for LLMs to give accurate, confident answers without needing to interpret whether "1.04" is good or bad.

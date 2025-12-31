# src/engine/grading.py

"""
CPK Grading System

Converts Cost Per Kill (CPK) values into letter grades (S-F tier).
Based on game duration analysis: median CPK ~2.5 across 5-turn games.

Lower CPK = More efficient = Better grade
"""

# Default grade thresholds (can be overridden)
DEFAULT_THRESHOLDS = {
    'S': 1.0,   # CPK <= 1.0: Can remove similarly costed units in single interaction
    'A': 1.5,   # CPK <= 1.5: Excellent trade efficiency
    'B': 2.0,   # CPK <= 2.0: Good trade efficiency
    'C': 2.5,   # CPK <= 2.5: Average (median) - neutral trades
    'D': 3.0,   # CPK <= 3.0: Below average - unfavorable trades
    'E': 3.5,   # CPK <= 3.5: Poor - very unfavorable trades
    'F': None   # CPK > 3.5: Ineffective - minimal game impact
}


def get_cpk_grade(cpk, thresholds=None):
    """
    Converts a CPK value to a letter grade.

    Args:
        cpk: Cost Per Kill value (float)
        thresholds: Optional dict of grade thresholds.
                   If None, uses DEFAULT_THRESHOLDS.

    Returns:
        str: Letter grade ('S', 'A', 'B', 'C', 'D', 'E', or 'F')

    Examples:
        >>> get_cpk_grade(0.8)
        'S'
        >>> get_cpk_grade(1.7)
        'B'
        >>> get_cpk_grade(4.2)
        'F'
    """
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    # Handle edge cases
    if cpk <= 0 or cpk >= 999:
        return 'F'

    # Check thresholds in order
    if cpk <= thresholds['S']:
        return 'S'
    elif cpk <= thresholds['A']:
        return 'A'
    elif cpk <= thresholds['B']:
        return 'B'
    elif cpk <= thresholds['C']:
        return 'C'
    elif cpk <= thresholds['D']:
        return 'D'
    elif cpk <= thresholds['E']:
        return 'E'
    else:
        return 'F'


def get_grade_color(grade):
    """
    Returns a color code for each grade (useful for visualizations).

    Args:
        grade: Letter grade ('S', 'A', 'B', 'C', 'D', 'E', or 'F')

    Returns:
        str: Hex color code
    """
    colors = {
        'S': '#2196F3',  # Blue (special tier)
        'A': '#00D084',  # Green
        'B': '#4CAF50',  # Light Green
        'C': '#FFC107',  # Yellow/Amber
        'D': '#FF9800',  # Orange
        'E': '#FF5722',  # Deep Orange
        'F': '#F44336'   # Red
    }
    return colors.get(grade, '#9E9E9E')  # Default gray


def get_grade_description(grade):
    """
    Returns a human-readable description for each grade.

    Args:
        grade: Letter grade ('S', 'A', 'B', 'C', 'D', 'E', or 'F')

    Returns:
        str: Description of what the grade means
    """
    descriptions = {
        'S': 'Elite - removes similarly costed units in one interaction',
        'A': 'Excellent trade efficiency',
        'B': 'Good trade efficiency',
        'C': 'Average - roughly neutral trades',
        'D': 'Below average - unfavorable trades',
        'E': 'Poor - very unfavorable trades',
        'F': 'Ineffective - minimal game impact'
    }
    return descriptions.get(grade, 'Unknown')


def format_cpk_with_grade(cpk, thresholds=None, include_description=False):
    """
    Formats CPK value with its letter grade.

    Args:
        cpk: Cost Per Kill value (float)
        thresholds: Optional custom thresholds
        include_description: If True, includes grade description

    Returns:
        str: Formatted string like "1.7 (B-tier)" or "1.7 (B-tier: Good efficiency)"

    Examples:
        >>> format_cpk_with_grade(1.7)
        '1.7 (B-tier)'
        >>> format_cpk_with_grade(1.7, include_description=True)
        '1.7 (B-tier: Good efficiency)'
    """
    grade = get_cpk_grade(cpk, thresholds)

    if include_description:
        desc = get_grade_description(grade)
        return f"{cpk:.2f} ({grade}-tier: {desc})"
    else:
        return f"{cpk:.2f} ({grade}-tier)"


def get_all_thresholds():
    """
    Returns a copy of the default thresholds for configuration purposes.

    Returns:
        dict: Copy of DEFAULT_THRESHOLDS
    """
    return DEFAULT_THRESHOLDS.copy()

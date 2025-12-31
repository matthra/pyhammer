"""
Example: Using the CPK Grading System

This file demonstrates how to use the grading system in your Streamlit
dashboard or other visualizations.
"""

from src.engine.grading import (
    get_cpk_grade,
    get_grade_color,
    get_grade_description,
    format_cpk_with_grade,
    get_all_thresholds,
    DEFAULT_THRESHOLDS
)

# Example 1: Basic grade lookup
cpk_value = 1.7
grade = get_cpk_grade(cpk_value)
print(f"CPK {cpk_value} = Grade {grade}")  # Output: CPK 1.7 = Grade B

# Example 2: Get color for visualization
color = get_grade_color(grade)
print(f"Color for grade {grade}: {color}")  # Output: #4CAF50 (green)

# Example 3: Get description
description = get_grade_description(grade)
print(f"Description: {description}")  # Output: Good trade efficiency

# Example 4: Formatted output
formatted = format_cpk_with_grade(cpk_value, include_description=True)
print(formatted)  # Output: 1.70 (B-tier: Good trade efficiency)

# Example 5: Custom thresholds (if you want to adjust the grading scale)
custom_thresholds = {
    'S': 0.8,   # Stricter S-tier
    'A': 1.3,
    'B': 1.8,
    'C': 2.3,
    'D': 2.8,
    'E': 3.3,
    'F': None
}
custom_grade = get_cpk_grade(1.0, thresholds=custom_thresholds)
print(f"With custom thresholds, CPK 1.0 = Grade {custom_grade}")  # Output: Grade A

# Example 6: Use in Streamlit (conceptual - add to app.py)
"""
import streamlit as st
from src.engine.grading import get_cpk_grade, get_grade_color

# After calculating CPK in your dataframe
df['Grade'] = df['CPK'].apply(get_cpk_grade)
df['Color'] = df['Grade'].apply(get_grade_color)

# Display with colored badges
for _, row in df.iterrows():
    st.markdown(
        f"**{row['Unit']}**: "
        f"<span style='background-color:{row['Color']};padding:2px 8px;border-radius:4px;'>"
        f"{row['Grade']}-tier</span>",
        unsafe_allow_html=True
    )
"""

# Example 7: Plotly integration (for charts.py)
"""
import plotly.graph_objects as go
from src.engine.grading import get_grade_color

# Color bars by grade
colors = [get_grade_color(grade) for grade in df['Grade']]

fig = go.Figure(data=[
    go.Bar(
        x=df['Unit'],
        y=df['CPK'],
        marker_color=colors,
        text=df['Grade'],
        textposition='auto'
    )
])
"""

print("\n" + "="*60)
print("See this file for integration examples!")
print("="*60)

import json
import os
import streamlit as st
import plotly.express as px

def load_themes():
    # Look for themes.json in the same folder as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    theme_file = os.path.join(current_dir, "themes.json")
    
    default_themes = {
        "Default (Backup)": {
            "template": "plotly_dark",
            "colors": ["#636EFA", "#EF553B", "#00CC96", "#AB63FA"]
        }
    }
    
    if os.path.exists(theme_file):
        try:
            with open(theme_file, "r") as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Could not load themes.json: {e}")
            return default_themes
    return default_themes

def get_unit_color_map(df, palette):
    """Assigns a consistent color to each unit based on the palette."""
    # Ensure UnitID exists
    df['UnitID'] = df['Name'] + " (" + df['Loadout Group'] + ")"
    unique_units = df['UnitID'].unique()
    unique_units.sort()
    
    color_map = {}
    for i, unit in enumerate(unique_units):
        color_map[unit] = palette[i % len(palette)]
    
    # Always set 'Other' to grey
    color_map['Other'] = '#777777'
    return color_map
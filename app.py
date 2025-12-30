import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup Path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 2. Imports
try:
    from src.data.targets import TARGETS
    from src.engine.calculator import calculate_group_metrics
    # NEW IMPORTS
    from src.visualizations.theme_utils import load_themes, get_unit_color_map
    from src.visualizations.charts import (
        plot_threat_matrix_interactive, 
        plot_efficiency_curve_interactive,
        plot_strength_profile,
        plot_army_damage
    )
except ModuleNotFoundError as e:
    st.error(f"CRITICAL ERROR: Could not import modules. \n\nError Details: {e}")
    st.stop()

st.set_page_config(page_title="PyHammer 0.3.7", page_icon="⚡", layout="wide")
st.title("⚡ PyHammer v0.3.7")

# --- LOAD CONFIG ---
THEMES = load_themes()

# --- INITIAL DATA ---
if 'roster' not in st.session_state:
    st.session_state['roster'] = pd.DataFrame([
        {
            'Name': 'War Dog Brigand', 'Loadout Group': 'Ranged', 'Pts': 170, 'Range': 24,
            'A': 2, 'BS': 2, 'S': 12, 'AP': -4, 'D': 'D6+4', 
            'Sustained':0, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        },
        {
            'Name': 'War Dog Brigand', 'Loadout Group': 'Ranged', 'Pts': 170, 'Range': 36,
            'A': 12, 'BS': 2, 'S': 6, 'AP': -1, 'D': '1', 
            'Sustained':0, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        },
        {
            'Name': 'War Dog Karnivore', 'Loadout Group': 'Melee', 'Pts': 140, 'Range': 'M',
            'A': 4, 'BS': 2, 'S': 12, 'AP': -3, 'D': 'D6+2', 
            'Sustained':0, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        }
    ])

# --- UI TABS ---
tab_build, tab_cpk, tab_kills, tab_ttk, tab_viz = st.tabs([
    "🏗️ Roster Manager", 
    "💰 Efficiency (CPK)", 
    "💀 Lethality (Kills)", 
    "⏱️ Time to Kill",
    "📊 Interactive Charts"
])

# --- TAB 1: BUILDER ---
with tab_build:
    edited_df = st.data_editor(st.session_state['roster'], num_rows="dynamic", width='stretch')
    st.session_state['roster'] = edited_df
    c1, c2 = st.columns(2)
    with c1: st.download_button("💾 Download CSV", edited_df.to_csv(index=False).encode('utf-8'), "roster.csv", "text/csv")
    with c2:
        up_file = st.file_uploader("📂 Import CSV", type=['csv'])
        if up_file:
            st.session_state['roster'] = pd.read_csv(up_file)
            st.rerun()

# --- HELPER: BUILD METRICS TABLE ---
def build_metric_df(metric_key):
    data = {}
    for t_key, t_stats in TARGETS.items():
        group_res = calculate_group_metrics(edited_df, t_stats)
        col_data = []
        index_names = []
        for g in group_res:
            index_names.append(f"{g['Unit']} [{g['Group']}]")
            col_data.append(g[metric_key])
        data['Unit'] = index_names
        data[t_key] = col_data
    if not data: return pd.DataFrame()
    return pd.DataFrame(data).set_index('Unit')

# --- METRIC TABS ---
with tab_cpk:
    if not edited_df.empty: st.dataframe(build_metric_df('CPK').style.background_gradient(cmap='RdYlGn_r', vmin=0.5, vmax=4.5), width='stretch', height=600)
with tab_kills:
    if not edited_df.empty: st.dataframe(build_metric_df('Kills').style.background_gradient(cmap='RdYlGn', vmin=0, vmax=10), width='stretch', height=600)
with tab_ttk:
    if not edited_df.empty: st.dataframe(build_metric_df('TTK').style.background_gradient(cmap='RdYlGn_r', vmin=0.5, vmax=4.0), width='stretch', height=600)

# --- TAB 5: VISUALIZATIONS ---
with tab_viz:
    if edited_df.empty:
        st.info("Add units to see charts.")
    else:
        # 1. Select Theme
        c_theme, c_spacer = st.columns([1, 4])
        with c_theme:
            theme_names = list(THEMES.keys())
            selected_theme_name = st.selectbox("🎨 Chart Theme", theme_names)
        
        # 2. Get Config from JSON
        theme_data = THEMES[selected_theme_name]
        chosen_template = theme_data.get("template", "plotly")
        chosen_palette = theme_data.get("colors", px.colors.qualitative.Bold)

        # 3. Generate Colors
        unit_colors = get_unit_color_map(edited_df, chosen_palette)
        
        # 4. Render Charts (Clean & Modular!)
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(plot_threat_matrix_interactive(edited_df, unit_colors, chosen_template), width='stretch')
        with c2: st.plotly_chart(plot_efficiency_curve_interactive(edited_df, unit_colors, chosen_template), width='stretch')
        
        st.divider()
        
        c3, c4 = st.columns(2)
        with c3: st.plotly_chart(plot_strength_profile(edited_df, chosen_template), width='stretch')
        with c4: st.plotly_chart(plot_army_damage(edited_df, unit_colors, chosen_template), width='stretch')
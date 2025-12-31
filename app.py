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

st.set_page_config(page_title="PyHammer 0.3.8", page_icon="⚡", layout="wide")

# --- SIDEBAR (Restored!) ---
with st.sidebar:
    st.title("⚡ PyHammer v0.3.8")
    st.markdown("---")
    st.header("🎯 Analysis Focus")
    
    # Select a target for the "Army Summary" and Charts
    target_keys = list(TARGETS.keys())
    # Default to "Marine Equivalent" or first available
    default_idx = target_keys.index("Marine Equivalent") if "Marine Equivalent" in target_keys else 0
    
    selected_target_key = st.selectbox("Enemy Profile", target_keys, index=default_idx)
    selected_target_stats = TARGETS[selected_target_key]
    
    # Show Stats for context
    c1, c2, c3 = st.columns(3)
    c1.metric("T", selected_target_stats['T'])
    c2.metric("Sv", f"{selected_target_stats['Sv']}+")
    c3.metric("W", selected_target_stats.get('W', 1))
    
    st.markdown("---")
    st.caption("v0.3.8 RC1 - Optimization Engine Active")

# --- LOAD CONFIG ---
THEMES = load_themes()

# --- INITIAL DATA ---
if 'roster' not in st.session_state:
    st.session_state['roster'] = pd.DataFrame([
        {
            'Qty': 1,
            'Name': 'War Dog Brigand', 'Loadout Group': 'Ranged', 'Pts': 170, 'Range': 24,
            'Profile ID': '', 
            'Weapon': 'Demonbreath Spear',
            'A': 2, 'BS': 2, 'S': 12, 'AP': -4, 'D': 'D6+4', 
            'CritHit': 6, 'CritWound': 6,
            'Sustained':0, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        },
        {
            'Qty': 1,
            'Name': 'War Dog Brigand', 'Loadout Group': 'Ranged', 'Pts': 170, 'Range': 36,
            'Profile ID': '',
            'Weapon': 'Avenger Chaincannon',
            'A': 12, 'BS': 2, 'S': 6, 'AP': -1, 'D': '1', 
            'CritHit': 6, 'CritWound': 6,
            'Sustained':0, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        },
        {
            'Qty': 1,
            'Name': 'War Dog Karnivore', 'Loadout Group': 'Melee', 'Pts': 140, 'Range': 'M',
            'Profile ID': 'Claw', 
            'Weapon': 'Reaper Chaintalon (Strike)',
            'A': 6, 'BS': 2, 'S': 12, 'AP': -3, 'D': 'D6+2', 
            'CritHit': 6, 'CritWound': 6, 
            'Sustained':1, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        },
        {
            'Qty': 1,
            'Name': 'War Dog Karnivore', 'Loadout Group': 'Melee', 'Pts': 140, 'Range': 'M',
            'Profile ID': 'Claw', 
            'Weapon': 'Reaper Chaintalon (Sweep)',
            'A': 12, 'BS': 2, 'S': 8, 'AP': -2, 'D': 1, 
            'CritHit': 6, 'CritWound': 6, 
            'Sustained':1, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'
        }
    ])

# --- ROBUST SANITIZATION ---
# 1. Retrieve data
raw_data = st.session_state.get('roster', pd.DataFrame())

# 2. DEFENSIVE TYPE CHECK
if not isinstance(raw_data, pd.DataFrame):
    try:
        raw_df = pd.DataFrame(raw_data)
    except Exception:
        raw_df = pd.DataFrame()
else:
    raw_df = raw_data

# 3. Clean Columns
if not raw_df.empty:
    # Ensure Numeric Columns
    if 'Pts' in raw_df.columns:
        raw_df['Pts'] = pd.to_numeric(raw_df['Pts'], errors='coerce').fillna(0)
    
    if 'Qty' in raw_df.columns:
        raw_df['Qty'] = pd.to_numeric(raw_df['Qty'], errors='coerce').fillna(1).astype(int)
    else:
        raw_df['Qty'] = 1
        
    if 'Profile ID' in raw_df.columns:
        raw_df['Profile ID'] = raw_df['Profile ID'].astype(str).replace('nan', '')
    else:
        raw_df['Profile ID'] = ''

    # Filter out rows with no Name
    if 'Name' in raw_df.columns:
        active_roster = raw_df.dropna(subset=['Name']).copy()
        active_roster = active_roster[active_roster['Name'].astype(str).str.strip() != '']
    else:
        active_roster = raw_df.copy()
else:
    active_roster = pd.DataFrame()

# 4. Save back to state
st.session_state['roster'] = active_roster
# This 'active_roster' is what we use for the rest of the app
edited_df = active_roster 

# --- MAIN LAYOUT ---
st.title("⚔️ Mathhammer Analysis")

# --- ARMY DASHBOARD ---
if not edited_df.empty:
    army_results = calculate_group_metrics(edited_df, selected_target_stats, deduplicate=False)
    army_df = pd.DataFrame(army_results)
    
    if not army_df.empty:
        total_dmg = army_df['Damage'].sum()
        total_kills = army_df['Kills'].sum()
        
        # --- POINTS FIX ---
        # We can't just sum(Pts * Qty) on the raw dataframe because of the duplicate rows.
        # Instead, we calculate it from our CLEAN 'army_results' which has already handled the grouping!
        
        # Each row in army_results represents a UNIT (with Qty applied).
        # We need to recalculate the total cost basis from that.
        # Logic: (Unit Pts * Qty) is implicitly what we want.
        # However, army_results doesn't return raw 'Pts', it used it for CPK.
        
        # Let's extract the cost from the CPK logic or re-calculate.
        # Re-calculating is safer:
        # Group raw DF by [Name, Qty], take MAX Pts, then Sum (Pts * Qty).
        
        pts_group = edited_df.groupby(['Name', 'Qty'])['Pts'].max().reset_index()
        roster_pts = (pts_group['Pts'] * pts_group['Qty']).sum()
        
        # Army Efficiency
        target_pts = selected_target_stats.get('Pts', 1)
        kill_value = total_kills * target_pts
        army_cpk = roster_pts / kill_value if kill_value > 0 else 0

        # KPI CARDS
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("🛡️ Total Army Points", f"{roster_pts}")
        k2.metric(f"💥 Damage vs {selected_target_key}", f"{total_dmg:.1f}")
        k3.metric(f"💀 Kills vs {selected_target_key}", f"{total_kills:.1f}")
        k4.metric("📈 Army CPK", f"{army_cpk:.2f}", delta_color="inverse")
    
    st.divider()

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
    # 1. File Uploader Callback
    def load_csv():
        if st.session_state.uploaded_file is not None:
            try:
                new_df = pd.read_csv(st.session_state.uploaded_file)
                # Force strings to avoid type issues
                for col in ['Name', 'Weapon', 'Loadout Group', 'Keywords', 'Profile ID']:
                    if col in new_df.columns:
                        new_df[col] = new_df[col].astype(str)
                st.session_state['roster'] = new_df
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

    # 2. The Editor (Capture the output directly)
    edited_input = st.data_editor(
        st.session_state['roster'], 
        num_rows="dynamic", 
        width='stretch',
        key='roster_editor'
    )
    
    # Safety Check: Ensure output is a DataFrame
    # (Fixes 'dict object has no attribute equals' error)
    if isinstance(edited_input, pd.DataFrame):
        edited_df = edited_input
    else:
        # Fallback if Streamlit returns a dict/list
        try:
            edited_df = pd.DataFrame(edited_input)
        except Exception:
            edited_df = st.session_state['roster'] # Revert to last known good state

    # 3. Sync Logic
    # Now we compare the clean 'edited_df' against the state
    if not edited_df.equals(st.session_state['roster']):
        st.session_state['roster'] = edited_df
        st.rerun()

    # 4. Buttons
    c1, c2 = st.columns(2)
    with c1: 
        st.download_button(
            "💾 Download CSV", 
            st.session_state['roster'].to_csv(index=False).encode('utf-8'), 
            "roster.csv", 
            "text/csv"
        )
    with c2:
        st.file_uploader(
            "📂 Import CSV", 
            type=['csv'], 
            key="uploaded_file", 
            on_change=load_csv
        )

# --- HELPER: BUILD METRICS TABLE ---
def build_metric_data(metric_key):
    """
    Returns TWO dataframes:
    1. df_values: The numeric stats (CPK, Kills, etc)
    2. df_tooltips: The text to show on hover (Active Profiles)
    """
    data = {}
    tooltips = {}
    
    # Iterate through all targets (columns)
    for t_key, t_stats in TARGETS.items():
        # Calculate stats for this target
        # deduplicate=True ensures we see 1 Unit Efficiency (ignoring Qty)
        group_res = calculate_group_metrics(edited_df, t_stats, deduplicate=True)
        
        col_data = []
        col_tips = []
        index_names = []
        
        for g in group_res:
            label = f"{g['Unit']} [{g['Group']}]"
            index_names.append(label)
            
            col_data.append(g[metric_key])
            
            if g.get('Mode'):
                col_tips.append(f"Active: {g['Mode']}")
            else:
                col_tips.append("Standard Profile")
                
        data['Unit'] = index_names
        tooltips['Unit'] = index_names
        
        data[t_key] = col_data
        tooltips[t_key] = col_tips
        
    if not data: return pd.DataFrame(), pd.DataFrame()
    
    df_values = pd.DataFrame(data).set_index('Unit')
    df_tips = pd.DataFrame(tooltips).set_index('Unit')
    
    return df_values, df_tips

# --- METRIC TABS ---
# Note: We removed the global 'show_modes' toggle from here.

with tab_cpk:
    st.caption("Lower is Better (Points Cost per Kill)")
    # Toggle specific to this tab
    show_modes_cpk = st.toggle("Show Active Weapon Profiles", key="toggle_cpk")
    
    if not edited_df.empty: 
        vals, tips = build_metric_data('CPK')
        if not vals.empty:
            st.dataframe(
                vals.style.background_gradient(cmap='RdYlGn_r', vmin=0.5, vmax=15.0)
                          .format("{:.2f}"), 
                width='stretch', 
                height=500
            )
            if show_modes_cpk:
                st.caption("👇 Active Weapon Profiles used for the calculations above:")
                st.dataframe(tips, width='stretch')

with tab_kills:
    st.caption("Higher is Better (Expected Kills per Activation)")
    # Toggle specific to this tab
    show_modes_kills = st.toggle("Show Active Weapon Profiles", key="toggle_kills")
    
    if not edited_df.empty: 
        vals, tips = build_metric_data('Kills')
        if not vals.empty:
            st.dataframe(
                vals.style.background_gradient(cmap='RdYlGn', vmin=0, vmax=5)
                          .format("{:.2f}"),
                width='stretch', 
                height=500
            )
            if show_modes_kills:
                st.caption("👇 Active Weapon Profiles used for the calculations above:")
                st.dataframe(tips, width='stretch')

with tab_ttk:
    st.caption("Lower is Better (Activations required to wipe unit)")
    # Toggle specific to this tab
    show_modes_ttk = st.toggle("Show Active Weapon Profiles", key="toggle_ttk")
    
    if not edited_df.empty: 
        vals, tips = build_metric_data('TTK')
        if not vals.empty:
            st.dataframe(
                vals.style.background_gradient(cmap='RdYlGn_r', vmin=0.5, vmax=4.0)
                          .format("{:.2f}"),
                width='stretch', 
                height=500
            )
            if show_modes_ttk:
                st.caption("👇 Active Weapon Profiles used for the calculations above:")
                st.dataframe(tips, width='stretch')

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
        
        # 4. Render Charts
        st.subheader(f"Analysis vs {selected_target_key}")
        
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(plot_threat_matrix_interactive(edited_df, unit_colors, chosen_template), width='stretch')
        with c2: st.plotly_chart(plot_efficiency_curve_interactive(edited_df, unit_colors, chosen_template), width='stretch')
        
        st.divider()
        
        c3, c4 = st.columns(2)
        with c3: st.plotly_chart(plot_strength_profile(edited_df, chosen_template), width='stretch')
        with c4: st.plotly_chart(plot_army_damage(edited_df, unit_colors, chosen_template), width='stretch')
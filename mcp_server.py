import sys
import os

# Force Python to look in the current directory
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- CORRECTED IMPORTS ---
try:
    from data.targets import TARGETS
    from engine.calculator import calculate_group_metrics
except ModuleNotFoundError as e:
    st.error(f"CRITICAL ERROR: Could not import modules. \n\nError Details: {e}")
    st.stop()

st.set_page_config(page_title="PyHammer 3.1", page_icon="⚡", layout="wide")
st.title("⚡ PyHammer v3.1")

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

# --- TAB ORDER ---
tab_build, tab_cpk, tab_kills, tab_ttk, tab_viz = st.tabs([
    "🏗️ Roster Builder", 
    "💰 Efficiency (CPK)", 
    "💀 Lethality (Kills)", 
    "⏱️ Time to Kill",
    "📊 Interactive Charts"
])

# --- CHART 1: THREAT MATRIX ---
def plot_threat_matrix_interactive(df):
    plot_data = df.copy()
    plot_data['Range'] = plot_data['Range'].replace({'M': 0, 'm': 0})
    plot_data['Range'] = pd.to_numeric(plot_data['Range'], errors='coerce').fillna(0)
    
    grouped = plot_data.groupby(['Range', 'S', 'AP']).agg({
        'A': 'sum', 
        'Name': lambda x: '<br>'.join(x.unique())
    }).reset_index()
    
    grouped['Hover_Text'] = (
        "<b>Units:</b> " + grouped['Name'] + "<br>" +
        "<b>Total Shots:</b> " + grouped['A'].astype(str) + "<br>" +
        "<b>Strength:</b> " + grouped['S'].astype(str) + "<br>" +
        "<b>AP:</b> " + grouped['AP'].astype(str)
    )

    fig = px.scatter(
        grouped, x='Range', y='S', size='A', color='AP',
        color_continuous_scale='RdYlBu', 
        title="<b>1. Threat Matrix</b> (Reach vs Strength)",
        hover_name='Hover_Text', size_max=60
    )

    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=6, range=[-2, 50], title="Range (Inches)"),
        yaxis=dict(title="Strength"), height=400, margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- CHART 2: EFFICIENCY CURVES ---
def plot_efficiency_curve_interactive(df):
    sorted_targets = sorted(TARGETS.items(), key=lambda item: item[1]['T'])
    target_names = [t[1]['Name'].split(' ')[0] for t in sorted_targets]
    target_keys = [t[0] for t in sorted_targets]
    
    records = []
    groups = df[['Name', 'Loadout Group']].drop_duplicates()
    
    for _, row in groups.iterrows():
        unit_name = row['Name']
        group_name = row['Loadout Group']
        subset_df = df[(df['Name'] == unit_name) & (df['Loadout Group'] == group_name)]
        
        for t_key, t_name in zip(target_keys, target_names):
            t_stats = TARGETS[t_key]
            metrics = calculate_group_metrics(subset_df, t_stats)
            val = metrics[0]['CPK'] if metrics else 0
            records.append({
                'Unit': f"{unit_name} ({group_name})",
                'Target': t_name,
                'CPK': min(val, 5.0)
            })
            
    long_df = pd.DataFrame(records)
    
    fig = px.line(
        long_df, x='Target', y='CPK', color='Unit', markers=True,
        title="<b>2. Efficiency Curves</b> (Lower is Better)"
    )

    fig.add_shape(type="rect", xref="paper", yref="y", x0=0, y0=0, x1=1, y1=2.0,
        fillcolor="green", opacity=0.1, layer="below", line_width=0)
    fig.add_hline(y=2.5, line_dash="dash", line_color="orange", annotation_text="Baseline")

    fig.add_annotation(xref="paper", yref="paper", x=1.00, y=1.05, text="Worse ⇧", showarrow=False, font=dict(color="gray"))
    fig.add_annotation(xref="paper", yref="paper", x=1.00, y=-0.15, text="Better ⇩", showarrow=False, font=dict(color="gray"))

    fig.update_layout(hovermode="x unified", yaxis=dict(range=[0, 5.0]), height=400, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# --- CHART 3: ROI SCATTER (Points vs Output) ---
def plot_roi_scatter(df):
    # We calculate average damage against a "Standard Marine" (MEQ) to compare raw output
    t_stats = TARGETS['MEQ']
    
    records = []
    groups = df[['Name', 'Loadout Group', 'Pts']].drop_duplicates()
    
    for _, row in groups.iterrows():
        unit_name = row['Name']
        group_name = row['Loadout Group']
        pts = row['Pts']
        subset_df = df[(df['Name'] == unit_name) & (df['Loadout Group'] == group_name)]
        
        # Calculate raw kills
        metrics = calculate_group_metrics(subset_df, t_stats)
        kills = metrics[0]['Kills'] if metrics else 0
        
        # Calculate Total Wounds (approximate from kills * W)
        total_dmg = kills * t_stats['W'] 
        
        records.append({
            'Unit': f"{unit_name} ({group_name})",
            'Points': pts,
            'Output': total_dmg,
            'Efficiency': metrics[0]['CPK'] if metrics else 0
        })
        
    roi_df = pd.DataFrame(records)
    
    fig = px.scatter(
        roi_df, x='Points', y='Output', color='Efficiency',
        color_continuous_scale='RdYlGn_r', # Green = Low CPK (Good)
        size='Output', # Bigger dots = More damage
        text='Unit',
        title="<b>3. ROI Analysis</b> (Points Cost vs. Damage Output)"
    )
    
    fig.update_traces(textposition='top center')
    fig.update_layout(
        xaxis=dict(title="Unit Cost (Pts)"),
        yaxis=dict(title="Total Wounds Dealt (vs MEQ)"),
        height=400, margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- CHART 4: ONE-SHOT TEST (TTK Bars) ---
def plot_ttk_bars(df):
    # We filter for Heavy Targets only
    heavy_targets = ['VEQ-L', 'VEQ-H', 'KEQ', 'TEQ']
    records = []
    
    groups = df[['Name', 'Loadout Group']].drop_duplicates()
    
    for _, row in groups.iterrows():
        unit_name = row['Name']
        group_name = row['Loadout Group']
        subset_df = df[(df['Name'] == unit_name) & (df['Loadout Group'] == group_name)]
        
        for t_key in heavy_targets:
            if t_key in TARGETS:
                t_stats = TARGETS[t_key]
                metrics = calculate_group_metrics(subset_df, t_stats)
                ttk = metrics[0]['TTK'] if metrics else 99
                
                records.append({
                    'Unit': f"{unit_name} ({group_name})",
                    'Target': t_stats['Name'].split(' ')[0],
                    'Activations': min(ttk, 5.0) # Cap for visual
                })
                
    bar_df = pd.DataFrame(records)
    
    fig = px.bar(
        bar_df, x='Target', y='Activations', color='Unit',
        barmode='group',
        title="<b>4. The One-Shot Test</b> (Activations to Kill)"
    )
    
    # Add Critical Threshold Lines
    fig.add_hline(y=1.05, line_dash="dot", line_color="green", annotation_text="One Shot (1.0)")
    fig.add_hline(y=2.05, line_dash="dot", line_color="orange", annotation_text="Two Volleys (2.0)")
    
    fig.update_layout(
        yaxis=dict(title="Activations (Lower is Better)", range=[0, 4]),
        height=400, margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- BUILDER TAB ---
with tab_build:
    edited_df = st.data_editor(st.session_state['roster'], num_rows="dynamic", width="stretch")
    st.session_state['roster'] = edited_df

    c1, c2 = st.columns(2)
    with c1:
        st.download_button("💾 Download CSV", edited_df.to_csv(index=False).encode('utf-8'), "roster.csv", "text/csv")
    with c2:
        up_file = st.file_uploader("📂 Import CSV", type=['csv'])
        if up_file:
            st.session_state['roster'] = pd.read_csv(up_file)
            st.rerun()

# --- METRIC TABS ---
def build_metric_df(metric_key):
    data = {}
    for t_key, t_stats in TARGETS.items():
        group_res = calculate_group_metrics(edited_df, t_stats)
        col_data = []
        index_names = []
        for g in group_res:
            label = f"{g['Unit']} [{g['Group']}]"
            index_names.append(label)
            col_data.append(g[metric_key])
        data['Unit'] = index_names
        data[t_key] = col_data
    if not data: return pd.DataFrame()
    return pd.DataFrame(data).set_index('Unit')

with tab_cpk:
    if not edited_df.empty:
        st.dataframe(build_metric_df('CPK').style.background_gradient(cmap='RdYlGn_r', vmin=0.5, vmax=4.5), width="stretch", height=600)
with tab_kills:
    if not edited_df.empty:
        st.dataframe(build_metric_df('Kills').style.background_gradient(cmap='RdYlGn', vmin=0, vmax=10), width="stretch", height=600)
with tab_ttk:
    if not edited_df.empty:
        st.dataframe(build_metric_df('TTK').style.background_gradient(cmap='RdYlGn_r', vmin=0.5, vmax=4.0), width="stretch", height=600)

# --- VISUALIZATION DASHBOARD ---
with tab_viz:
    if edited_df.empty:
        st.info("Add units to see charts.")
    else:
        # Row 1
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(plot_threat_matrix_interactive(edited_df), use_container_width=True)
        with c2: st.plotly_chart(plot_efficiency_curve_interactive(edited_df), use_container_width=True)
        
        st.divider()
        
        # Row 2
        c3, c4 = st.columns(2)
        with c3: st.plotly_chart(plot_roi_scatter(edited_df), use_container_width=True)
        with c4: st.plotly_chart(plot_ttk_bars(edited_df), use_container_width=True)
import pandas as pd
import plotly.express as px
import sys
import os

# Adjust path to find engine if needed, though app.py usually sets path.
# Assuming this runs inside the app context where sys.path is set, 
# but good practice to import relative if inside a package.
from src.data.targets import TARGETS
from src.engine.calculator import calculate_group_metrics

# --- CHART 1: THREAT MATRIX ---
def plot_threat_matrix_interactive(df, color_map, template):
    plot_data = df.copy()
    plot_data['Range'] = plot_data['Range'].replace({'M': 0, 'm': 0})
    plot_data['Range'] = pd.to_numeric(plot_data['Range'], errors='coerce').fillna(0)
    plot_data['UnitID'] = plot_data['Name'] + " (" + plot_data['Loadout Group'] + ")"
    
    grouped = plot_data.groupby(['Range', 'S', 'UnitID']).agg({
        'A': 'sum', 'AP': 'mean'
    }).reset_index()
    
    grouped['Hover_Text'] = (
        "<b>Unit:</b> " + grouped['UnitID'] + "<br>" +
        "<b>Total Shots:</b> " + grouped['A'].astype(str) + "<br>" +
        "<b>Strength:</b> " + grouped['S'].astype(str)
    )

    fig = px.scatter(
        grouped, x='Range', y='S', size='A', 
        color='UnitID', 
        color_discrete_map=color_map,
        title="<b>1. Threat Matrix</b> (Reach vs Strength)",
        hover_name='Hover_Text', size_max=60,
        template=template
    )

    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=6, range=[-2, 50], title="Range (Inches)"),
        yaxis=dict(title="Strength"), height=400, margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title=None)
    )
    return fig

# --- CHART 2: EFFICIENCY CURVES ---
def plot_efficiency_curve_interactive(df, color_map, template):
    sorted_targets = sorted(TARGETS.items(), key=lambda item: item[1]['T'])
    target_names = [t[1]['Name'].split(' ')[0] for t in sorted_targets]
    target_keys = [t[0] for t in sorted_targets]
    
    records = []
    groups = df[['Name', 'Loadout Group']].drop_duplicates()
    
    for _, row in groups.iterrows():
        unit_name = row['Name']
        group_name = row['Loadout Group']
        subset_df = df[(df['Name'] == unit_name) & (df['Loadout Group'] == group_name)]
        unit_id = f"{unit_name} ({group_name})"
        
        for t_key, t_name in zip(target_keys, target_names):
            t_stats = TARGETS[t_key]
            metrics = calculate_group_metrics(subset_df, t_stats)
            val = metrics[0]['CPK'] if metrics else 0
            records.append({
                'UnitID': unit_id,
                'Target': t_name,
                'CPK': min(val, 5.0)
            })
            
    long_df = pd.DataFrame(records)
    
    fig = px.line(
        long_df, x='Target', y='CPK', 
        color='UnitID', 
        color_discrete_map=color_map,
        markers=True,
        title="<b>2. Efficiency Curves</b> (Lower is Better)",
        template=template
    )

    fig.add_hline(y=2.5, line_dash="dash", line_color="orange", annotation_text="Baseline")
    
    text_color = "gray" if "dark" not in template else "lightgray"
    fig.add_annotation(xref="paper", yref="paper", x=1.00, y=1.05, text="Worse ⇧", showarrow=False, font=dict(color=text_color))
    fig.add_annotation(xref="paper", yref="paper", x=1.00, y=-0.15, text="Better ⇩", showarrow=False, font=dict(color=text_color))

    fig.update_layout(
        hovermode="x unified", yaxis=dict(range=[0, 5.0]), height=400, 
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title=None)
    )
    return fig

# --- CHART 3: STRENGTH & AP PROFILE ---
def plot_strength_profile(df, template):
    plot_df = df.copy()
    plot_df['AP_Label'] = "AP" + plot_df['AP'].astype(str)
    
    grouped = plot_df.groupby(['S', 'AP_Label', 'AP']).agg({'A': 'sum'}).reset_index()
    grouped = grouped.sort_values(by=['S', 'AP'], ascending=[True, True])

    bar_colors = px.colors.sequential.Magma_r
    if "dark" in template:
        bar_colors = px.colors.sequential.Viridis

    fig = px.bar(
        grouped, x='S', y='A', color='AP_Label',
        title="<b>3. Strength & AP Profile</b> (Volume of Fire)",
        labels={'S': 'Strength', 'A': 'Total Shots', 'AP_Label': 'AP'},
        text_auto=True,
        color_discrete_sequence=bar_colors,
        template=template
    )

    fig.update_layout(
        xaxis=dict(type='category', title="Strength"),
        yaxis=dict(title="Number of Shots"),
        legend=dict(title="AP Value"),
        height=400, margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- CHART 4: ARMY DAMAGE (Top 4 + Other) ---
def plot_army_damage(df, color_map, template):
    sorted_targets = sorted(TARGETS.items(), key=lambda item: item[1]['T'])
    target_names = [t[1]['Name'].split(' ')[0] for t in sorted_targets]
    target_keys = [t[0] for t in sorted_targets]
    
    records = []
    
    for t_key, t_name in zip(target_keys, target_names):
        t_stats = TARGETS[t_key]
        
        unit_damages = []
        groups = df[['Name', 'Loadout Group']].drop_duplicates()
        
        for _, row in groups.iterrows():
            unit_name = row['Name']
            group_name = row['Loadout Group']
            subset_df = df[(df['Name'] == unit_name) & (df['Loadout Group'] == group_name)]
            unit_id = f"{unit_name} ({group_name})"
            
            metrics = calculate_group_metrics(subset_df, t_stats)
            kills = metrics[0]['Kills'] if metrics else 0
            dmg = kills * t_stats['W']
            
            if dmg > 0:
                unit_damages.append({'UnitID': unit_id, 'Damage': dmg})
                
        unit_damages.sort(key=lambda x: x['Damage'], reverse=True)
        
        top_n = 4
        for i, item in enumerate(unit_damages):
            if i < top_n:
                records.append({
                    'Target': t_name,
                    'UnitID': item['UnitID'],
                    'Damage': item['Damage'],
                    'Rank': i
                })
            else:
                records.append({
                    'Target': t_name,
                    'UnitID': 'Other',
                    'Damage': item['Damage'],
                    'Rank': 99
                })

    plot_df = pd.DataFrame(records)
    if not plot_df.empty:
        plot_df = plot_df.groupby(['Target', 'UnitID', 'Rank']).agg({'Damage': 'sum'}).reset_index()
        plot_df = plot_df.sort_values(by=['Rank'], ascending=True)

    fig = px.bar(
        plot_df, x='Target', y='Damage', 
        color='UnitID',
        color_discrete_map=color_map,
        title="<b>4. Total Army Output</b> (Top Contributors per Target)",
        template=template
    )
    
    fig.update_layout(
        yaxis=dict(title="Total Wounds Dealt"),
        height=400, margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title=None),
        barmode='stack'
    )
    return fig
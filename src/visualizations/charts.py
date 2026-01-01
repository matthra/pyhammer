import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data.targets import TARGETS
from src.engine.calculator import calculate_group_metrics, parse_d6_value

# --- HELPER: DATA SANITIZATION ---
def safe_chart_data(df):
    """
    Creates a copy of the dataframe with guaranteed numeric columns for plotting.
    - 'A', 'S', 'Range' are converted to floats (averages).
    - 'M' in Range becomes 0.
    - 'AP' is ensured to be numeric.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    plot_df = df.copy()
    
    # 1. Clean 'A' (Attacks) -> Used for Bubble Size
    # Parse "D6" -> 3.5
    if 'A' in plot_df.columns:
        plot_df['A_Num'] = plot_df['A'].apply(parse_d6_value).astype(float)
    else:
        plot_df['A_Num'] = 1.0

    # 2. Clean 'S' (Strength) -> Used for Y-Axis
    if 'S' in plot_df.columns:
        plot_df['S_Num'] = plot_df['S'].apply(parse_d6_value).astype(float)
    else:
        plot_df['S_Num'] = 4.0

    # 3. Clean 'Range' -> Used for X-Axis
    if 'Range' in plot_df.columns:
        # Handle 'M' or 'Melee' manually first
        plot_df['Range_Num'] = plot_df['Range'].astype(str).str.upper().replace({'M': '0', 'MELEE': '0'})
        plot_df['Range_Num'] = plot_df['Range_Num'].apply(parse_d6_value).astype(float)
    else:
        plot_df['Range_Num'] = 24.0
        
    # 4. Clean 'AP'
    if 'AP' in plot_df.columns:
        # Ensure AP is numeric (handle '-1' string vs -1 int)
        plot_df['AP_Num'] = pd.to_numeric(plot_df['AP'], errors='coerce').fillna(0)
    else:
        plot_df['AP_Num'] = 0

    # 5. Clean 'Qty' -> Used for Multiplier
    if 'Qty' in plot_df.columns:
        plot_df['Qty_Num'] = pd.to_numeric(plot_df['Qty'], errors='coerce').fillna(1)
    else:
        plot_df['Qty_Num'] = 1.0
        
    return plot_df

# --- CHART 1: THREAT MATRIX ---
def plot_threat_matrix_interactive(df, color_map, template):
    # 1. Sanitize first
    clean_df = safe_chart_data(df)
    
    # 2. Create Display Columns
    clean_df['UnitID'] = clean_df['Name'] + " (" + clean_df['Loadout Group'] + ")"
    
    # 3. Group by Numeric Values for plotting
    grouped = clean_df.groupby(['Range_Num', 'S_Num', 'UnitID', 'Name']).agg({
        'A_Num': 'sum', 
        'AP_Num': 'mean'
    }).reset_index()
    
    # 4. Build Custom Hover Text
    grouped['Hover_Text'] = (
        "<b>Unit:</b> " + grouped['UnitID'] + "<br>" +
        "<b>Total Shots:</b> " + grouped['A_Num'].astype(str) + "<br>" +
        "<b>Strength:</b> " + grouped['S_Num'].astype(str) + "<br>" +
        "<b>Avg AP:</b> " + grouped['AP_Num'].astype(str)
    )

    fig = px.scatter(
        grouped, 
        x='Range_Num', 
        y='S_Num', 
        size='A_Num', 
        color='Name', # Use Name to match the color_map keys
        color_discrete_map=color_map,
        title="<b>1. Threat Matrix</b> (Reach vs Strength)",
        hover_name='Hover_Text', 
        size_max=60,
        template=template
    )

    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=6, range=[-2, 50], title="Range (Inches)"),
        yaxis=dict(title="Strength"), 
        height=400, 
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title=None)
    )
    return fig

# --- CHART 2: EFFICIENCY CURVES ---
def plot_efficiency_curve_interactive(df, color_map, template, assume_half_range=False):
    # Sort targets by Toughness for a logical X-Axis
    sorted_targets = sorted(TARGETS.items(), key=lambda item: item[1]['T'])
    target_names = [t[1]['Name'].split(' ')[0] for t in sorted_targets]
    target_keys = [t[0] for t in sorted_targets]

    records = []
    # Identify unique groups
    groups = df[['Name', 'Loadout Group']].drop_duplicates()

    for _, row in groups.iterrows():
        unit_name = row['Name']
        group_name = row['Loadout Group']
        # Use boolean indexing mask
        subset_df = df[(df['Name'] == unit_name) & (df['Loadout Group'] == group_name)]
        unit_id = f"{unit_name} ({group_name})"

        for t_key, t_name in zip(target_keys, target_names):
            t_stats = TARGETS[t_key]
            # Calc metrics (Using the robust engine)
            metrics = calculate_group_metrics(subset_df, t_stats, deduplicate=True, assume_half_range=assume_half_range) # True = Efficiency
            val = metrics[0]['CPK'] if metrics else 0

            records.append({
                'UnitID': unit_id,
                'Name': unit_name, # Needed for color mapping
                'Target': t_name,
                'CPK': min(val, 5.0) # Cap at 5.0 for readability
            })
            
    long_df = pd.DataFrame(records)
    
    if long_df.empty:
        return go.Figure()

    fig = px.line(
        long_df, 
        x='Target', 
        y='CPK', 
        color='Name', # Match color map
        line_group='UnitID', # Allows multiple lines per color if needed
        color_discrete_map=color_map,
        markers=True,
        title="<b>2. Efficiency Curves</b> (Lower is Better)",
        template=template
    )

    # Annotations
    fig.add_hline(y=1.0, line_dash="dash", line_color="green", opacity=0.5)
    
    text_color = "gray" if "dark" in str(template).lower() else "lightgray"
    fig.add_annotation(xref="paper", yref="paper", x=1.00, y=1.05, text="Worse ⇧", showarrow=False, font=dict(color=text_color))
    fig.add_annotation(xref="paper", yref="paper", x=1.00, y=-0.15, text="Better ⇩", showarrow=False, font=dict(color=text_color))

    fig.update_layout(
        hovermode="x unified", 
        yaxis=dict(range=[0, 5.0], title="CPK (Cost per Kill)"), 
        height=400, 
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title=None)
    )
    return fig

# --- CHART 3: STRENGTH & AP PROFILE ---
def plot_strength_profile(df, template):
    # Sanitize
    clean_df = safe_chart_data(df)
    
    clean_df['AP_Label'] = "AP" + clean_df['AP_Num'].astype(int).astype(str)
    
    # --- FIX: Apply Qty Multiplier ---
    clean_df['Total_Shots'] = clean_df['A_Num'] * clean_df['Qty_Num']
    
    # Group by sanitized numeric columns, SUMMING 'Total_Shots'
    grouped = clean_df.groupby(['S_Num', 'AP_Label', 'AP_Num']).agg({'Total_Shots': 'sum'}).reset_index()
    grouped = grouped.sort_values(by=['S_Num', 'AP_Num'], ascending=[True, True])

    bar_colors = px.colors.sequential.Magma_r
    if "dark" in str(template).lower():
        bar_colors = px.colors.sequential.Viridis

    fig = px.bar(
        grouped, 
        x='S_Num', 
        y='Total_Shots',  # Changed from A_Num
        color='AP_Label',
        title="<b>3. Strength & AP Profile</b> (Volume of Fire)",
        labels={'S_Num': 'Strength', 'Total_Shots': 'Total Shots', 'AP_Label': 'AP'},
        text_auto=True,
        color_discrete_sequence=bar_colors,
        template=template
    )

    fig.update_layout(
        xaxis=dict(type='category', title="Strength"),
        yaxis=dict(title="Number of Shots"),
        legend=dict(title="AP Value"),
        height=400, 
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- CHART 4: ARMY DAMAGE (Top 4 + Other) ---
def plot_army_damage(df, color_map, template, assume_half_range=False):
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

            # Use deduplicate=False to get TOTAL ARMY DAMAGE
            metrics = calculate_group_metrics(subset_df, t_stats, deduplicate=False, assume_half_range=assume_half_range)
            kills = metrics[0]['Kills'] if metrics else 0
            dmg = kills * t_stats.get('W', 1)
            
            if dmg > 0:
                unit_damages.append({
                    'UnitID': unit_id, 
                    'Name': unit_name,
                    'Damage': dmg
                })
                
        unit_damages.sort(key=lambda x: x['Damage'], reverse=True)
        
        top_n = 4
        for i, item in enumerate(unit_damages):
            if i < top_n:
                records.append({
                    'Target': t_name,
                    'UnitID': item['UnitID'],
                    'Name': item['Name'],
                    'Damage': item['Damage'],
                    'Rank': i
                })
            else:
                records.append({
                    'Target': t_name,
                    'UnitID': 'Other',
                    'Name': 'Other',
                    'Damage': item['Damage'],
                    'Rank': 99
                })

    plot_df = pd.DataFrame(records)
    
    if plot_df.empty:
        return go.Figure()

    # Consolidate "Other" buckets if necessary, otherwise just plot
    plot_df = plot_df.groupby(['Target', 'UnitID', 'Name', 'Rank']).agg({'Damage': 'sum'}).reset_index()
    plot_df = plot_df.sort_values(by=['Rank'], ascending=True)

    fig = px.bar(
        plot_df, 
        x='Target', 
        y='Damage', 
        color='Name', # Match color map
        color_discrete_map=color_map,
        title="<b>4. Total Army Output</b> (Top Contributors per Target)",
        template=template
    )
    
    fig.update_layout(
        yaxis=dict(title="Total Wounds Dealt"),
        height=400, 
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(title=None),
        barmode='stack'
    )
    return fig
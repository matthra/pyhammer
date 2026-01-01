import sys
import os
import uuid
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup Path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 2. Imports
try:
    from src.data.targets import TARGETS
    from src.data.rosters import DEFAULT_ROSTER
    from src.data.target_manager import (
        get_available_target_lists,
        load_target_list,
        save_target_list,
        delete_target_list,
        get_target_list_metadata,
        validate_target_profile,
        import_targets_from_csv,
        export_targets_to_csv
    )
    from src.data.roster_manager import (
        get_available_rosters,
        load_roster_file,
        save_roster_file,
        delete_roster,
        get_roster_metadata,
        validate_roster_data,
        create_empty_roster
    )
    from src.engine.calculator import calculate_group_metrics
    from src.engine.grading import get_cpk_grade, get_grade_color
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

# --- SIDEBAR: GLOBAL CONFIGURATION ---
with st.sidebar:
    st.title("⚡ PyHammer v0.3.9")
    st.markdown("---")

    # === TARGET LIST SELECTION ===
    st.header("🎯 Target Profile")

    # Initialize active target list in session state
    if 'active_target_list' not in st.session_state:
        st.session_state['active_target_list'] = 'default'

    # Get available target lists
    available_lists = get_available_target_lists()

    # 1. SAFETY CHECK: Handle empty directory
    if not available_lists:
        st.error("CRITICAL ERROR: No target configuration files found in 'target_configs/'.")
        st.stop()

    # Target list dropdown logic
    active_list_name = st.session_state['active_target_list']

    # 2. SMART FALLBACK: If the current active list is missing or invalid
    if active_list_name not in available_lists:
        # Check if 'default' exists (or default.json)
        if 'default' in available_lists:
            active_list_name = 'default'
        elif 'default.json' in available_lists:
             active_list_name = 'default.json'
        else:
            # If neither exists, just grab the FIRST file found so the app doesn't crash
            active_list_name = available_lists[0]
            
        # Save the valid name back to session state
        st.session_state['active_target_list'] = active_list_name

    # 3. BUILD DISPLAY NAMES (This was missing)
    list_display_names = []
    for list_name in available_lists:
        try:
            metadata = get_target_list_metadata(list_name)
            list_display_names.append(metadata['name'])
        except:
            list_display_names.append(list_name)

    # 4. GET INDEX (Now safe)
    active_list_idx = available_lists.index(active_list_name)

    # 5. RENDER DROPDOWN
    selected_list_display = st.selectbox(
        "Target List",
        list_display_names,
        index=active_list_idx,
        key="target_list_selector"
    )

    # Update active list if changed
    selected_list_name = available_lists[list_display_names.index(selected_list_display)]
    prev_target_list = st.session_state.get('active_target_list')
    if selected_list_name != prev_target_list:
        st.session_state['active_target_list'] = selected_list_name
        st.toast(f"📋 Target list changed to: {selected_list_display}", icon="🎯")

    # Load targets from selected list
    try:
        target_list_data = load_target_list(selected_list_name)
        ACTIVE_TARGETS = target_list_data['targets']
    except:
        # Fallback to default TARGETS
        ACTIVE_TARGETS = TARGETS

    # Enemy profile dropdown (from active list)
    target_keys = list(ACTIVE_TARGETS.keys())

    # Track previous target for change detection
    if 'prev_target_key' not in st.session_state:
        st.session_state['prev_target_key'] = target_keys[0] if target_keys else None

    default_idx = target_keys.index("Marine Equivalent") if "Marine Equivalent" in target_keys else 0
    selected_target_key = st.selectbox("Enemy Profile", target_keys, index=default_idx, label_visibility="collapsed")

    # Detect target change
    if selected_target_key != st.session_state.get('prev_target_key'):
        st.session_state['prev_target_key'] = selected_target_key
        st.toast(f"🎯 Target changed to: {selected_target_key}", icon="🎯")

    selected_target_stats = ACTIVE_TARGETS[selected_target_key].copy()

    st.markdown("---")

    # === GLOBAL MODIFIERS ===
    st.header("⚙️ Global Settings")

    # Initialize toggles in session state
    if 'assume_cover' not in st.session_state:
        st.session_state['assume_cover'] = False
    if 'assume_half_range' not in st.session_state:
        st.session_state['assume_half_range'] = False

    # Track previous values for change detection
    prev_cover = st.session_state['assume_cover']
    prev_half_range = st.session_state['assume_half_range']

    # Cover Toggle
    assume_cover = st.checkbox(
        "🪨 Assume Cover",
        value=st.session_state['assume_cover'],
        key='cover_checkbox',
        help="Apply +1 to armor save for all targets (simulates light cover/ruins)"
    )

    # Detect cover toggle change
    if assume_cover != prev_cover:
        if assume_cover:
            st.toast("✅ Cover enabled - Calculations updated (+1 to all saves)", icon="🪨")
        else:
            st.toast("❌ Cover disabled - Calculations updated", icon="🪨")

    st.session_state['assume_cover'] = assume_cover

    # Half Range Toggle
    assume_half_range = st.checkbox(
        "📏 Assume Half Range",
        value=st.session_state['assume_half_range'],
        key='half_range_checkbox',
        help="Apply Melta and Rapid Fire bonuses globally (close combat engagement)"
    )

    # Detect half range toggle change
    if assume_half_range != prev_half_range:
        if assume_half_range:
            st.toast("✅ Half Range enabled - Melta & Rapid Fire bonuses applied", icon="📏")
        else:
            st.toast("❌ Half Range disabled - Calculations updated", icon="📏")

    st.session_state['assume_half_range'] = assume_half_range

    # Apply cover bonus if enabled
    if assume_cover:
        current_save = selected_target_stats.get('Sv', '7+')
        try:
            save_val = int(current_save.replace('+', ''))
            improved_save = max(2, save_val - 1)  # Cover: +1 save, min 2+
            selected_target_stats['Sv'] = f'{improved_save}+'
        except:
            pass

    st.markdown("---")

    # === DATA IMPORT/EXPORT ===
    st.header("📂 Data Management")

    # Targets CSV Import
    with st.expander("Import Custom Targets"):
        st.caption("Upload a CSV with custom target profiles (T, Sv, W, etc.)")
        targets_file = st.file_uploader("Targets CSV", type=['csv'], key="targets_csv", label_visibility="collapsed")
        if targets_file:
            st.info("Custom target import feature coming soon!")
            # TODO: Implement custom target loading

    # === ROSTER MANAGEMENT ===
    st.header("📊 Roster Management")

    # Initialize current roster file in session state
    if 'current_roster_file' not in st.session_state:
        st.session_state['current_roster_file'] = 'default_roster'

    # Get available rosters
    available_rosters = get_available_rosters()

    # Roster selection dropdown
    selected_roster = st.selectbox(
        "Select Roster",
        available_rosters,
        index=available_rosters.index(st.session_state['current_roster_file'])
              if st.session_state['current_roster_file'] in available_rosters else 0,
        key='roster_selector'
    )

    # Load roster when selection changes
    if selected_roster != st.session_state['current_roster_file']:
        try:
            st.session_state['roster'] = load_roster_file(selected_roster)
            st.session_state['current_roster_file'] = selected_roster
            st.toast(f"✅ Loaded roster: {selected_roster}", icon="📊")
            # No explicit rerun needed - selectbox change triggers automatic rerun
        except Exception as e:
            st.error(f"Error loading roster: {e}")

    # Roster action buttons
    col1, col2 = st.columns(2)

    with col1:
        # New Roster button
        if st.button("📁 New Roster", use_container_width=True):
            st.session_state['roster'] = create_empty_roster()
            st.session_state['current_roster_file'] = 'new_roster'
            st.toast("✅ Created new roster", icon="📁")
            # Button click triggers automatic rerun

    with col2:
        # Delete Roster button
        if st.button("🗑️ Delete", use_container_width=True,
                     disabled=(st.session_state['current_roster_file'] == 'default_roster')):
            # Show confirmation in session state
            st.session_state['confirm_delete'] = True

    # Delete confirmation dialog
    if st.session_state.get('confirm_delete', False):
        st.warning(f"⚠️ Delete '{st.session_state['current_roster_file']}'?")
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            if st.button("✅ Yes, Delete", use_container_width=True):
                deleted_name = st.session_state['current_roster_file']
                if delete_roster(deleted_name):
                    st.session_state['current_roster_file'] = 'default_roster'
                    st.session_state['roster'] = load_roster_file('default_roster')
                    st.session_state['confirm_delete'] = False
                    st.toast(f"🗑️ Deleted roster: {deleted_name}", icon="✅")
                    # Button click triggers automatic rerun
                else:
                    st.error("❌ Cannot delete this roster")
                    st.session_state['confirm_delete'] = False
        with dcol2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state['confirm_delete'] = False
                # Button click triggers automatic rerun

    # Save roster name input (for new rosters or save as)
    if st.session_state['current_roster_file'] in ['new_roster', '']:
        roster_name = st.text_input(
            "Roster Name",
            value="my_roster",
            help="Name for saving this roster"
        )
    else:
        roster_name = st.session_state['current_roster_file']

    # Save and Save & Recalculate buttons
    save_col1, save_col2 = st.columns(2)

    with save_col1:
        if st.button("💾 Save", use_container_width=True):
            try:
                # Validate before saving
                is_valid, error_msg = validate_roster_data(st.session_state['roster'])
                if not is_valid:
                    st.error(f"❌ Cannot save: {error_msg}")
                else:
                    saved_name = save_roster_file(
                        st.session_state['roster'],
                        roster_name,
                        description="",
                        overwrite=True
                    )
                    st.session_state['current_roster_file'] = saved_name
                    st.toast(f"💾 Saved: {saved_name}", icon="✅")
            except Exception as e:
                st.error(f"Error saving roster: {e}")

    with save_col2:
        if st.button("💾 Save & Recalculate", use_container_width=True, type="primary"):
            try:
                # Validate before saving
                is_valid, error_msg = validate_roster_data(st.session_state['roster'])
                if not is_valid:
                    st.error(f"❌ Cannot save: {error_msg}")
                else:
                    # Save the roster
                    saved_name = save_roster_file(
                        st.session_state['roster'],
                        roster_name,
                        description="",
                        overwrite=True
                    )
                    st.session_state['current_roster_file'] = saved_name
                    st.toast(f"💾 Saved & recalculated: {saved_name}", icon="✅")
                    # Button click triggers automatic rerun - calculations will update
            except Exception as e:
                st.error(f"Error saving roster: {e}")

    st.markdown("---")
    st.caption("v0.3.9 - Global Config Update")

# --- LOAD CONFIG ---
THEMES = load_themes()

# --- INITIAL DATA ---
if 'roster' not in st.session_state:
    # Load default roster from JSON file
    try:
        st.session_state['roster'] = load_roster_file('default_roster')
    except Exception as e:
        # Fallback to hardcoded DEFAULT_ROSTER if file doesn't exist
        st.warning(f"Could not load default_roster.json, using fallback: {e}")
        st.session_state['roster'] = pd.DataFrame(DEFAULT_ROSTER)

# --- ROBUST SANITIZATION ---
# 1. Retrieve data
raw_data = st.session_state.get('roster', pd.DataFrame())

if not isinstance(raw_data, pd.DataFrame):
    raw_df = pd.DataFrame()
else:
    raw_df = raw_data

if not raw_df.empty:
    # 1. Clean Numeric Columns
    if 'Pts' in raw_df.columns:
        raw_df['Pts'] = pd.to_numeric(raw_df['Pts'], errors='coerce').fillna(0)
    if 'Qty' in raw_df.columns:
        raw_df['Qty'] = pd.to_numeric(raw_df['Qty'], errors='coerce').fillna(1).astype(int)
    
    # 2. Clean Text Columns
    for col in ['Name', 'Weapon', 'Loadout Group', 'Profile ID']:
        if col in raw_df.columns:
            raw_df[col] = raw_df[col].astype(str).replace('nan', '')
            
    # 3. --- UNIT ID GENERATION (The Logic Fix) ---
    if 'UnitID' not in raw_df.columns:
        # LEGACY IMPORT DETECTED:
        # We assume rows with the exact same Name belong to the same Unit.
        # We assign a new random UUID to each unique Name group.
        raw_df['UnitID'] = raw_df.groupby('Name')['Name'].transform(lambda x: str(uuid.uuid4()))
    else:
        # If ID column exists but some rows are empty (partial data), fill them
        raw_df['UnitID'] = raw_df['UnitID'].fillna('').astype(str)
        mask_missing = raw_df['UnitID'] == ''
        if mask_missing.any():
            # Assign unique IDs to orphans to be safe
            raw_df.loc[mask_missing, 'UnitID'] = [str(uuid.uuid4()) for _ in range(mask_missing.sum())]

    # Filter invalid rows
    if 'Name' in raw_df.columns:
        active_roster = raw_df.dropna(subset=['Name']).copy()
        active_roster = active_roster[active_roster['Name'].str.strip() != '']
    else:
        active_roster = raw_df.copy()
else:
    active_roster = pd.DataFrame()

st.session_state['roster'] = active_roster
edited_df = active_roster

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
    # Debug indicator for half range mode
    if assume_half_range:
        st.info("📏 Half Range Mode: ACTIVE - Melta and Rapid Fire bonuses are applied")

    army_results = calculate_group_metrics(edited_df, selected_target_stats, deduplicate=False, assume_half_range=assume_half_range)
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
tab_build, tab_cpk, tab_kills, tab_ttk, tab_viz, tab_targets = st.tabs([
    "🏗️ Roster Manager",
    "💰 Efficiency (CPK)",
    "💀 Lethality (Kills)",
    "⏱️ Time to Kill",
    "📊 Interactive Charts",
    "🎯 Target Manager"
])

# --- TAB 1: BUILDER (Master-Detail View) ---
with tab_build:
    # Layout: Master List (Left) | Detail Editor (Right)
    c_list, c_detail = st.columns([1, 2])
    
    # --- LEFT: MASTER LIST ---
    with c_list:
        st.subheader("📋 My Units")
        
        if not st.session_state['roster'].empty:
            # 1. Prepare the Data
            # We group by UnitID to get unique entries
            grouped = st.session_state['roster'].groupby('UnitID').agg({
                'Name': 'first',
                'Qty': 'first',
                'Pts': 'first',
                'Weapon': 'count'
            }).reset_index()
            
            # 2. State Management for Selection
            # We use session_state to track which ID is 'active' across reruns
            if 'selected_unit_id' not in st.session_state:
                st.session_state['selected_unit_id'] = None

            # 3. Render Buttons (The "Navigation List")
            # We iterate through the units and create a button for each.
            for idx, row in grouped.iterrows():
                u_id = row['UnitID']
                
                # Calculate display values
                total_pts = row['Pts'] * row['Qty']
                label = f"{row['Name']} (x{row['Qty']}) - {total_pts}pts"
                
                # Determine button style (Highlight the active one)
                is_active = (u_id == st.session_state['selected_unit_id'])
                btn_type = "primary" if is_active else "secondary"
                
                # Render the button
                if st.button(label, key=f"btn_{u_id}", type=btn_type, use_container_width=True):
                    st.session_state['selected_unit_id'] = u_id
                    st.rerun()

            # Set the ID for the right panel to use
            active_unit_id = st.session_state['selected_unit_id']
            
        else:
            st.info("Roster is empty.")
            active_unit_id = None

        st.divider()
        
        # New Unit Button
        if st.button("➕ New Unit", use_container_width=True):
            new_id = str(uuid.uuid4())
            new_row = {
                'UnitID': new_id, 'Qty': 1, 'Name': 'New Unit', 'Pts': 100,
                'Weapon': 'New Weapon', 'Range': '24', 'A': '4', 'BS': '3', 'S': '4', 'AP': 0, 'D': '1',
                'Loadout Group': 'Ranged', 'Profile ID': '', 'Keywords': '',
                'CritHit': 6, 'CritWound': 6, 'Sustained': 0, 'Lethal': 'N', 'Dev': 'N',
                'Torrent': 'N', 'TwinLinked': 'N', 'Blast': 'N', 'Melta': 'N', 'RapidFire': 'N', 'RR_H': 'N', 'RR_W': 'N'
            }
            st.session_state['roster'] = pd.concat([st.session_state['roster'], pd.DataFrame([new_row])], ignore_index=True)
            # Auto-select the new unit
            st.session_state['selected_unit_id'] = new_id
            st.rerun()

    # --- RIGHT: DETAIL EDITOR ---
    with c_detail:
        if active_unit_id:
            # Get all rows for this unit
            unit_mask = st.session_state['roster']['UnitID'] == active_unit_id
            unit_rows = st.session_state['roster'][unit_mask].copy()
            first_row = unit_rows.iloc[0]
            
            # --- HEADER (Shared Stats) ---
            st.subheader(f"🛠️ Editing: {first_row['Name']}")
            
            with st.form("unit_header_form"):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                u_name = c1.text_input("Unit Name", value=first_row['Name'])
                u_qty = c2.number_input("Qty", min_value=1, value=int(first_row['Qty']))
                u_pts = c3.number_input("Pts (per model)", min_value=0, value=int(first_row['Pts']))
                
                c4.markdown("<br>", unsafe_allow_html=True)
                delete_btn = c4.form_submit_button("🗑️ Delete Unit", type="primary")

                if st.form_submit_button("💾 Update Unit Details"):
                    # Update ALL rows with this ID
                    st.session_state['roster'].loc[unit_mask, 'Name'] = u_name
                    st.session_state['roster'].loc[unit_mask, 'Qty'] = u_qty
                    st.session_state['roster'].loc[unit_mask, 'Pts'] = u_pts
                    st.success("Unit updated.")
                    st.rerun()
                
                if delete_btn:
                    # Remove all rows with this ID
                    st.session_state['roster'] = st.session_state['roster'][~unit_mask]
                    st.rerun()

            st.divider()
            
            # --- WEAPON EDITOR (Loop through rows) ---
            st.caption(f"Weapons ({len(unit_rows)})")
            
            for idx, row in unit_rows.iterrows():
                # Each weapon gets an Expander
                label = f"⚔️ {row['Weapon']} ({row['Loadout Group']})"
                with st.expander(label, expanded=False):
                    with st.form(f"wep_form_{idx}"):
                        w_name = st.text_input("Weapon Name", value=row['Weapon'])
                        
                        c1, c2, c3 = st.columns(3)
                        w_type = c1.selectbox("Type", ["Ranged", "Melee"], index=0 if row['Loadout Group'] == 'Ranged' else 1)
                        w_rng = c2.text_input("Range", value=str(row['Range']))
                        w_pid = c3.text_input("Profile ID", value=str(row['Profile ID']), help="Use matching IDs for exclusive modes (e.g. 'Plasma')")
                        
                        s1, s2, s3, s4, s5 = st.columns(5)
                        w_a = s1.text_input("A", value=str(row['A']))
                        
                        # BS Handling
                        curr_bs = str(row['BS']).replace('+', '')
                        bs_opts = ["2", "3", "4", "5", "6", "N/A"]
                        bs_idx = bs_opts.index(curr_bs) if curr_bs in bs_opts else 1
                        w_bs = s2.selectbox("BS/WS", bs_opts, index=bs_idx)
                        
                        w_s = s3.text_input("S", value=str(row['S']))
                        
                        # AP Handling
                        curr_ap = int(row['AP']) if str(row['AP']).lstrip('-').isdigit() else 0
                        ap_opts = [0, -1, -2, -3, -4, -5, -6]
                        ap_idx = ap_opts.index(curr_ap) if curr_ap in ap_opts else 0
                        w_ap = s4.selectbox("AP", ap_opts, index=ap_idx)
                        
                        w_d = s5.text_input("D", value=str(row['D']))

                        # Keywords Section
                        st.caption("⚙️ Keywords & Special Rules")
                        k1, k2, k3, k4 = st.columns(4)

                        # Get current values (with defaults)
                        curr_lethal = str(row.get('Lethal', 'N')).upper() == 'Y'
                        curr_dev = str(row.get('Dev', 'N')).upper() == 'Y'
                        curr_torrent = str(row.get('Torrent', 'N')).upper() == 'Y'
                        curr_twin = str(row.get('TwinLinked', 'N')).upper() == 'Y'

                        w_lethal = k1.checkbox("Lethal Hits", value=curr_lethal, help="Critical hits auto-wound")
                        w_dev = k2.checkbox("Devastating Wounds", value=curr_dev, help="Critical wounds become mortal wounds")
                        w_torrent = k3.checkbox("Torrent", value=curr_torrent, help="Auto-hit (ignores BS)")
                        w_twin = k4.checkbox("Twin-Linked", value=curr_twin, help="Reroll wound rolls")

                        k5, k6, k7, k8 = st.columns(4)
                        curr_blast = str(row.get('Blast', 'N')).upper() == 'Y'
                        w_blast = k5.checkbox("Blast", value=curr_blast, help="Bonus attacks vs large units (6+ models)")

                        # Parse Melta value: 'Y'/'N' (legacy) or number
                        melta_val = str(row.get('Melta', '0')).upper()
                        if melta_val == 'Y':
                            curr_melta = 1
                        elif melta_val == 'N' or melta_val == '':
                            curr_melta = 0
                        else:
                            curr_melta = int(melta_val) if melta_val.isdigit() else 0
                        w_melta = k6.number_input("Melta", min_value=0, max_value=6, value=curr_melta, help="Add X flat damage at half range (e.g., Melta 4 = +4 damage)")

                        # Parse Rapid Fire value: 'Y'/'N' (legacy) or number
                        rapid_fire_val = str(row.get('RapidFire', '0')).upper()
                        if rapid_fire_val == 'Y':
                            curr_rapid_fire = 1  # Legacy 'Y' = Rapid Fire 1
                        elif rapid_fire_val == 'N' or rapid_fire_val == '':
                            curr_rapid_fire = 0
                        else:
                            curr_rapid_fire = int(rapid_fire_val) if rapid_fire_val.isdigit() else 0
                        w_rapid_fire = k7.number_input("Rapid Fire", min_value=0, max_value=6, value=curr_rapid_fire, help="Add X extra attacks at half range (e.g., Rapid Fire 1 = +1 attack)")

                        curr_sustained = int(row.get('Sustained', 0)) if str(row.get('Sustained', 0)).isdigit() else 0
                        w_sustained = k8.number_input("Sustained Hits", min_value=0, max_value=6, value=curr_sustained, help="Extra hits on critical")

                        # Advanced: Critical thresholds
                        with st.expander("🎯 Advanced: Critical Thresholds"):
                            t1, t2 = st.columns(2)
                            curr_crit_hit = int(row.get('CritHit', 6)) if str(row.get('CritHit', 6)).isdigit() else 6
                            curr_crit_wound = int(row.get('CritWound', 6)) if str(row.get('CritWound', 6)).isdigit() else 6
                            w_crit_hit = t1.number_input("Critical Hit", min_value=2, max_value=6, value=curr_crit_hit, help="Hit roll needed for crit")
                            w_crit_wound = t2.number_input("Critical Wound", min_value=2, max_value=6, value=curr_crit_wound, help="Wound roll needed for crit")

                        # Save/Delete
                        c_save, c_del = st.columns([1, 1])
                        save_wep = c_save.form_submit_button("Save Changes")
                        del_wep = c_del.form_submit_button("Remove Weapon", type="primary")

                        if save_wep:
                            st.session_state['roster'].at[idx, 'Weapon'] = w_name
                            st.session_state['roster'].at[idx, 'Loadout Group'] = w_type
                            st.session_state['roster'].at[idx, 'Range'] = w_rng
                            st.session_state['roster'].at[idx, 'Profile ID'] = w_pid
                            st.session_state['roster'].at[idx, 'A'] = w_a
                            st.session_state['roster'].at[idx, 'BS'] = w_bs
                            st.session_state['roster'].at[idx, 'S'] = w_s
                            st.session_state['roster'].at[idx, 'AP'] = w_ap
                            st.session_state['roster'].at[idx, 'D'] = w_d

                            # Save keywords
                            st.session_state['roster'].at[idx, 'Lethal'] = 'Y' if w_lethal else 'N'
                            st.session_state['roster'].at[idx, 'Dev'] = 'Y' if w_dev else 'N'
                            st.session_state['roster'].at[idx, 'Torrent'] = 'Y' if w_torrent else 'N'
                            st.session_state['roster'].at[idx, 'TwinLinked'] = 'Y' if w_twin else 'N'
                            st.session_state['roster'].at[idx, 'Blast'] = 'Y' if w_blast else 'N'
                            st.session_state['roster'].at[idx, 'Melta'] = str(w_melta) if w_melta > 0 else 'N'
                            st.session_state['roster'].at[idx, 'RapidFire'] = str(w_rapid_fire) if w_rapid_fire > 0 else 'N'
                            st.session_state['roster'].at[idx, 'Sustained'] = w_sustained
                            st.session_state['roster'].at[idx, 'CritHit'] = w_crit_hit
                            st.session_state['roster'].at[idx, 'CritWound'] = w_crit_wound

                            st.rerun()
                        
                        if del_wep:
                            st.session_state['roster'] = st.session_state['roster'].drop(idx).reset_index(drop=True)
                            st.rerun()

            # --- ADD NEW WEAPON ---
            if st.button("➕ Add Weapon Profile", use_container_width=True):
                new_wep = first_row.copy()
                new_wep['Weapon'] = "New Weapon"
                # Keep UnitID/Name/Qty so it stays linked!
                st.session_state['roster'] = pd.concat([st.session_state['roster'], pd.DataFrame([new_wep])], ignore_index=True)
                st.rerun()

        else:
            # Empty State (Right Panel)
            st.info("👈 Select a unit from the list to edit its loadout.")
            st.caption("Or click 'New Unit' to create a dataslate.")

# --- HELPER: GRADE-BASED STYLING ---
def style_cpk_by_grade(val):
    """
    Returns background color based on CPK grade.
    Maps S-tier (blue) to F-tier (red).
    """
    if pd.isna(val) or val >= 999:
        return 'background-color: #9E9E9E'  # Gray for invalid

    grade = get_cpk_grade(val)
    color = get_grade_color(grade)
    return f'background-color: {color}'

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

    # Use map instead of deprecated applymap
    try:
        return df_cpk.map(cpk_to_color)
    except AttributeError:
        # Fallback for older pandas versions
        return df_cpk.applymap(cpk_to_color)

# --- HELPER: BUILD METRICS TABLE ---
def build_metric_data(metric_key, include_cpk=False, assume_half_range=False):
    """
    Returns TWO or THREE dataframes:
    1. df_values: The numeric stats (CPK, Kills, etc)
    2. df_tooltips: The text to show on hover (Active Profiles)
    3. df_cpk: (Optional) CPK values for styling purposes
    """
    data = {}
    tooltips = {}
    cpk_data = {} if include_cpk else None

    # Iterate through all targets (columns)
    for t_key, t_stats in ACTIVE_TARGETS.items():
        # Calculate stats for this target
        # deduplicate=True ensures we see 1 Unit Efficiency (ignoring Qty)
        group_res = calculate_group_metrics(edited_df, t_stats, deduplicate=True, assume_half_range=assume_half_range)

        col_data = []
        col_tips = []
        col_cpk = [] if include_cpk else None
        index_names = []

        for g in group_res:
            label = f"{g['Unit']} [{g['Group']}]"
            index_names.append(label)

            col_data.append(g[metric_key])

            if include_cpk:
                col_cpk.append(g['CPK'])

            if g.get('Mode'):
                col_tips.append(f"Active: {g['Mode']}")
            else:
                col_tips.append("Standard Profile")

        data['Unit'] = index_names
        tooltips['Unit'] = index_names

        data[t_key] = col_data
        tooltips[t_key] = col_tips

        if include_cpk:
            cpk_data['Unit'] = index_names
            cpk_data[t_key] = col_cpk

    if not data:
        if include_cpk:
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        return pd.DataFrame(), pd.DataFrame()

    df_values = pd.DataFrame(data).set_index('Unit')
    df_tips = pd.DataFrame(tooltips).set_index('Unit')

    if include_cpk:
        df_cpk = pd.DataFrame(cpk_data).set_index('Unit')
        return df_values, df_tips, df_cpk

    return df_values, df_tips

# --- METRIC TABS ---

with tab_cpk:
    st.caption("Lower is Better (Points Cost per Kill) - Color coded by efficiency grade")

    # Grade Legend
    with st.expander("📊 Grade Scale Reference"):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        grades = [
            ('S', '≤1.0', '#2196F3', 'Elite'),
            ('A', '≤1.5', '#00D084', 'Excellent'),
            ('B', '≤2.0', '#4CAF50', 'Good'),
            ('C', '≤2.5', '#FFC107', 'Average'),
            ('D', '≤3.0', '#FF9800', 'Below Avg'),
            ('E', '≤3.5', '#FF5722', 'Poor'),
            ('F', '>3.5', '#F44336', 'Ineffective')
        ]
        for col, (grade, cpk_range, color, desc) in zip([col1, col2, col3, col4, col5, col6, col7], grades):
            with col:
                st.markdown(f"<div style='background-color:{color};padding:8px;border-radius:4px;text-align:center;'>"
                           f"<b>{grade}</b><br><small>{cpk_range}</small><br><small>{desc}</small></div>",
                           unsafe_allow_html=True)

    if not edited_df.empty:
        vals, tips = build_metric_data('CPK', assume_half_range=assume_half_range)
        if not vals.empty:
            # Active Weapon Profiles (Collapsible)
            with st.expander("🔧 Active Weapon Profiles"):
                st.caption("Weapon profiles used for the calculations below (after profile optimization):")
                st.dataframe(tips, width='stretch', height=200)

            # The Main Table with Grade-Based Colors
            st.dataframe(
                vals.style.map(style_cpk_by_grade)
                          .format("{:.2f}"),
                width='stretch',
                height=500
            )

with tab_kills:
    st.caption("Higher is Better (Expected Kills per Activation) - Color coded by efficiency grade")

    # Grade Legend
    with st.expander("📊 Grade Scale Reference"):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        grades = [
            ('S', '≤1.0', '#2196F3', 'Elite'),
            ('A', '≤1.5', '#00D084', 'Excellent'),
            ('B', '≤2.0', '#4CAF50', 'Good'),
            ('C', '≤2.5', '#FFC107', 'Average'),
            ('D', '≤3.0', '#FF9800', 'Below Avg'),
            ('E', '≤3.5', '#FF5722', 'Poor'),
            ('F', '>3.5', '#F44336', 'Ineffective')
        ]
        for col, (grade, cpk_range, color, desc) in zip([col1, col2, col3, col4, col5, col6, col7], grades):
            with col:
                st.markdown(f"<div style='background-color:{color};padding:8px;border-radius:4px;text-align:center;'>"
                           f"<b>{grade}</b><br><small>{cpk_range}</small><br><small>{desc}</small></div>",
                           unsafe_allow_html=True)

    if not edited_df.empty:
        vals, tips, cpk_vals = build_metric_data('Kills', include_cpk=True, assume_half_range=assume_half_range)
        if not vals.empty:
            # Active Weapon Profiles (Collapsible)
            with st.expander("🔧 Active Weapon Profiles"):
                st.caption("Weapon profiles used for the calculations below (after profile optimization):")
                st.dataframe(tips, width='stretch', height=200)

            # Apply CPK-based styling to Kills table
            styles = get_cpk_background_colors(cpk_vals)
            st.dataframe(
                vals.style.apply(lambda _: styles, axis=None)
                          .format("{:.2f}"),
                width='stretch',
                height=500
            )

with tab_ttk:
    st.caption("Lower is Better (Activations required to wipe unit) - Color coded by efficiency grade")

    # Grade Legend
    with st.expander("📊 Grade Scale Reference"):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        grades = [
            ('S', '≤1.0', '#2196F3', 'Elite'),
            ('A', '≤1.5', '#00D084', 'Excellent'),
            ('B', '≤2.0', '#4CAF50', 'Good'),
            ('C', '≤2.5', '#FFC107', 'Average'),
            ('D', '≤3.0', '#FF9800', 'Below Avg'),
            ('E', '≤3.5', '#FF5722', 'Poor'),
            ('F', '>3.5', '#F44336', 'Ineffective')
        ]
        for col, (grade, cpk_range, color, desc) in zip([col1, col2, col3, col4, col5, col6, col7], grades):
            with col:
                st.markdown(f"<div style='background-color:{color};padding:8px;border-radius:4px;text-align:center;'>"
                           f"<b>{grade}</b><br><small>{cpk_range}</small><br><small>{desc}</small></div>",
                           unsafe_allow_html=True)

    if not edited_df.empty:
        vals, tips, cpk_vals = build_metric_data('TTK', include_cpk=True, assume_half_range=assume_half_range)
        if not vals.empty:
            # Active Weapon Profiles (Collapsible)
            with st.expander("🔧 Active Weapon Profiles"):
                st.caption("Weapon profiles used for the calculations below (after profile optimization):")
                st.dataframe(tips, width='stretch', height=200)

            # Apply CPK-based styling to TTK table
            styles = get_cpk_background_colors(cpk_vals)
            st.dataframe(
                vals.style.apply(lambda _: styles, axis=None)
                          .format("{:.2f}"),
                width='stretch',
                height=500
            )

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
        with c2: st.plotly_chart(plot_efficiency_curve_interactive(edited_df, unit_colors, chosen_template, assume_half_range), width='stretch')

        st.divider()

        c3, c4 = st.columns(2)
        with c3: st.plotly_chart(plot_strength_profile(edited_df, chosen_template), width='stretch')
        with c4: st.plotly_chart(plot_army_damage(edited_df, unit_colors, chosen_template, assume_half_range), width='stretch')# Target Manager Tab Implementation
# This will be appended to app.py

# --- TAB 6: TARGET MANAGER ---
with tab_targets:
    st.header("🎯 Target Manager")
    st.caption("Create and manage custom target lists for different meta environments")

    # Initialize session state for target manager
    if 'editing_target_list' not in st.session_state:
        st.session_state['editing_target_list'] = 'default'
    if 'editing_profile_name' not in st.session_state:
        st.session_state['editing_profile_name'] = None
    if 'creating_new_list' not in st.session_state:
        st.session_state['creating_new_list'] = False

    # Three column layout
    col_lists, col_editor, col_preview = st.columns([1, 2, 1])

    # --- LEFT PANEL: TARGET LISTS ---
    with col_lists:
        st.subheader("📋 Target Lists")

        # Get available lists
        available_lists = get_available_target_lists()

        # Display each list
        for list_name in available_lists:
            try:
                metadata = get_target_list_metadata(list_name)

                # Check if this list is active
                is_active = (list_name == st.session_state.get('active_target_list', 'default'))
                is_editing = (list_name == st.session_state['editing_target_list'])

                # Create columns for each list item
                cols = st.columns([1, 5, 2])

                with cols[0]:
                    if is_active:
                        st.write("✓")

                with cols[1]:
                    btn_type = "primary" if is_editing else "secondary"
                    if st.button(metadata['name'], key=f"edit_list_{list_name}", type=btn_type, use_container_width=True):
                        st.session_state['editing_target_list'] = list_name
                        st.session_state['editing_profile_name'] = None
                        st.session_state['creating_new_list'] = False
                        st.rerun()

                with cols[2]:
                    if is_active:
                        st.caption("Active")
                    else:
                        st.caption(f"{metadata['profile_count']} profiles")

            except Exception as e:
                st.error(f"Error loading {list_name}: {e}")

        st.divider()

        # Create new list button
        if st.button("➕ Create New List", use_container_width=True):
            st.session_state['creating_new_list'] = True
            st.session_state['editing_profile_name'] = None
            st.rerun()

        # Import/Export buttons
        st.divider()
        st.caption("Import/Export")

        # CSV Import
        uploaded_csv = st.file_uploader("Import from CSV", type=['csv'], key="import_targets_csv")
        if uploaded_csv is not None:
            try:
                csv_content = uploaded_csv.read().decode('utf-8')
                imported_targets = import_targets_from_csv(csv_content)

                if imported_targets:
                    st.success(f"Imported {len(imported_targets)} profiles")
                    # Store in session state for user to save
                    st.session_state['imported_targets'] = imported_targets
                else:
                    st.warning("No valid profiles found in CSV")
            except Exception as e:
                st.error(f"Error importing CSV: {e}")

    # --- CENTER PANEL: EDITOR ---
    with col_editor:
        # Mode 1: Creating new list
        if st.session_state['creating_new_list']:
            st.subheader("Create New Target List")

            with st.form("new_list_form"):
                new_list_name = st.text_input("List Name", placeholder="e.g., GT Meta 2025")
                new_list_desc = st.text_area("Description", placeholder="e.g., Common competitive tournament profiles")

                col_submit, col_cancel = st.columns(2)
                with col_submit:
                    create_btn = st.form_submit_button("Create List", type="primary", use_container_width=True)
                with col_cancel:
                    cancel_btn = st.form_submit_button("Cancel", use_container_width=True)

                if create_btn and new_list_name:
                    try:
                        # Create empty target list
                        filename = save_target_list(new_list_name, {}, new_list_desc)
                        st.success(f"Created '{new_list_name}'")
                        st.session_state['editing_target_list'] = filename
                        st.session_state['creating_new_list'] = False
                        st.rerun()
                    except FileExistsError:
                        st.error(f"List '{new_list_name}' already exists")
                    except Exception as e:
                        st.error(f"Error creating list: {e}")

                if cancel_btn:
                    st.session_state['creating_new_list'] = False
                    st.rerun()

        # Mode 2: Editing existing list
        else:
            editing_list_name = st.session_state['editing_target_list']

            try:
                list_data = load_target_list(editing_list_name)
                targets = list_data['targets']
                is_readonly = list_data.get('readonly', False)

                st.subheader(f"Editing: {list_data['name']}")

                if is_readonly:
                    st.info("ℹ️ This is a built-in list (read-only). Duplicate to create a custom version.")

                # Profile selector
                profile_names = list(targets.keys())

                if profile_names:
                    # Select profile to edit
                    selected_profile = st.selectbox(
                        "Select Profile to Edit",
                        profile_names,
                        index=profile_names.index(st.session_state['editing_profile_name']) if st.session_state['editing_profile_name'] in profile_names else 0,
                        key="profile_selector"
                    )

                    st.session_state['editing_profile_name'] = selected_profile

                    # Profile editor form
                    profile_data = targets[selected_profile]

                    with st.form(f"edit_profile_{selected_profile}"):
                        st.caption("Basic Stats")

                        col1, col2 = st.columns(2)
                        with col1:
                            edit_T = st.number_input("Toughness (T)", min_value=1, max_value=14, value=int(profile_data.get('T', 4)))
                            edit_Sv = st.selectbox("Save (Sv)", ["2+", "3+", "4+", "5+", "6+", "7+", "N"], index=["2+", "3+", "4+", "5+", "6+", "7+", "N"].index(str(profile_data.get('Sv', '3+'))))
                        with col2:
                            edit_W = st.number_input("Wounds (W)", min_value=1, max_value=30, value=int(profile_data.get('W', 2)))
                            edit_Pts = st.number_input("Points (Pts)", min_value=1, max_value=1000, value=int(profile_data.get('Pts', 20)))

                        edit_UnitSize = st.number_input("Unit Size", min_value=1, max_value=30, value=int(profile_data.get('UnitSize', 10)))

                        st.caption("Special Rules")
                        col3, col4, col5 = st.columns(3)
                        with col3:
                            # Handle both 'Invuln' and 'Inv' keys, convert empty string to 'N'
                            invuln_val = profile_data.get('Invuln', profile_data.get('Inv', 'N'))
                            invuln_val = 'N' if invuln_val == '' else str(invuln_val)
                            edit_Invuln = st.selectbox("Invuln Save", ["N", "2+", "3+", "4+", "5+", "6+"], index=["N", "2+", "3+", "4+", "5+", "6+"].index(invuln_val))
                        with col4:
                            # Convert empty string to 'N'
                            fnp_val = profile_data.get('FNP', 'N')
                            fnp_val = 'N' if fnp_val == '' else str(fnp_val)
                            edit_FNP = st.selectbox("Feel No Pain", ["N", "4+", "5+", "6+"], index=["N", "4+", "5+", "6+"].index(fnp_val))
                        with col5:
                            # Convert empty string to 'N'
                            stealth_val = profile_data.get('Stealth', 'N')
                            stealth_val = 'N' if stealth_val == '' else str(stealth_val)
                            edit_Stealth = st.selectbox("Stealth", ["N", "Y"], index=["N", "Y"].index(stealth_val))

                        if is_readonly:
                            # Show a dummy submit button for read-only forms to avoid Streamlit warning
                            st.form_submit_button("Read-Only (Cannot Edit)", disabled=True, use_container_width=True)
                            save_btn = False
                            delete_btn = False
                        else:
                            col_save, col_delete = st.columns(2)
                            with col_save:
                                save_btn = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                            with col_delete:
                                delete_btn = st.form_submit_button("🗑️ Delete Profile", use_container_width=True)

                        if save_btn and not is_readonly:
                            # Update profile - use 'Inv' to match JSON structure
                            updated_profile = {
                                'Name': profile_data.get('Name', ''),
                                'T': edit_T,
                                'Sv': edit_Sv,
                                'W': edit_W,
                                'UnitSize': edit_UnitSize,
                                'Pts': edit_Pts,
                                'Inv': edit_Invuln,
                                'FNP': edit_FNP,
                                'Stealth': edit_Stealth
                            }

                            targets[selected_profile] = updated_profile
                            save_target_list(editing_list_name, targets, list_data.get('description', ''), overwrite=True)
                            st.success(f"Updated '{selected_profile}'")
                            st.rerun()

                        if delete_btn and not is_readonly:
                            # Delete profile
                            del targets[selected_profile]
                            save_target_list(editing_list_name, targets, list_data.get('description', ''), overwrite=True)
                            st.session_state['editing_profile_name'] = None
                            st.success(f"Deleted '{selected_profile}'")
                            st.rerun()

                st.divider()

                # Add new profile
                if not is_readonly:
                    with st.expander("➕ Add New Profile"):
                        with st.form("add_new_profile"):
                            new_profile_name = st.text_input("Profile Name", placeholder="e.g., Space Marines")

                            col1, col2 = st.columns(2)
                            with col1:
                                new_T = st.number_input("T", min_value=1, max_value=14, value=4)
                                new_Sv = st.selectbox("Sv", ["2+", "3+", "4+", "5+", "6+", "7+", "N"], index=2)
                            with col2:
                                new_W = st.number_input("W", min_value=1, max_value=30, value=2)
                                new_Pts = st.number_input("Pts", min_value=1, max_value=1000, value=20)

                            new_UnitSize = st.number_input("Unit Size", min_value=1, max_value=30, value=10)

                            col6, col7, col8 = st.columns(3)
                            with col6:
                                new_Invuln = st.selectbox("Invuln", ["N", "2+", "3+", "4+", "5+", "6+"], index=0)
                            with col7:
                                new_FNP = st.selectbox("FNP", ["N", "4+", "5+", "6+"], index=0)
                            with col8:
                                new_Stealth = st.selectbox("Stealth", ["N", "Y"], index=0)

                            add_btn = st.form_submit_button("Add Profile", type="primary")

                            if add_btn and new_profile_name:
                                if new_profile_name in targets:
                                    st.error(f"Profile '{new_profile_name}' already exists")
                                else:
                                    new_profile = {
                                        'Name': new_profile_name,
                                        'T': new_T,
                                        'Sv': new_Sv,
                                        'W': new_W,
                                        'UnitSize': new_UnitSize,
                                        'Pts': new_Pts,
                                        'Inv': new_Invuln,
                                        'FNP': new_FNP,
                                        'Stealth': new_Stealth
                                    }

                                    targets[new_profile_name] = new_profile
                                    save_target_list(editing_list_name, targets, list_data.get('description', ''), overwrite=True)
                                    st.success(f"Added '{new_profile_name}'")
                                    st.rerun()

            except Exception as e:
                st.error(f"Error loading target list: {e}")

    # --- RIGHT PANEL: PREVIEW & ACTIONS ---
    with col_preview:
        st.subheader("📊 Preview")

        try:
            editing_list_name = st.session_state['editing_target_list']
            list_data = load_target_list(editing_list_name)
            targets = list_data['targets']

            # Summary metrics
            profile_count = len(targets)
            avg_pts = sum(p.get('Pts', 0) for p in targets.values()) / profile_count if profile_count > 0 else 0

            st.metric("Profiles", profile_count)
            st.metric("Avg Points", f"{avg_pts:.0f}")

            st.divider()

            # List all profiles
            st.caption("Profiles in this list:")
            for name, profile in targets.items():
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"• {name}")
                with cols[1]:
                    st.caption(f"{profile.get('Pts', 0)}pts")

            st.divider()

            # Actions
            is_active = (editing_list_name == st.session_state.get('active_target_list', 'default'))
            is_readonly = list_data.get('readonly', False)

            if not is_active:
                if st.button("✓ Set as Active", type="primary", use_container_width=True):
                    st.session_state['active_target_list'] = editing_list_name
                    st.success(f"Activated '{list_data['name']}'")
                    st.rerun()
            else:
                st.info("✓ This list is active")

            # Export to CSV
            if st.button("📤 Export to CSV", use_container_width=True):
                csv_content = export_targets_to_csv(targets)
                st.download_button(
                    "Download CSV",
                    csv_content,
                    f"{editing_list_name}.csv",
                    "text/csv",
                    use_container_width=True
                )

            # Delete list
            if not is_readonly and not is_active:
                if st.button("🗑️ Delete List", use_container_width=True):
                    if delete_target_list(editing_list_name):
                        st.success(f"Deleted '{list_data['name']}'")
                        st.session_state['editing_target_list'] = 'default'
                        st.rerun()
                    else:
                        st.error("Cannot delete this list")

        except Exception as e:
            st.error(f"Error in preview: {e}")

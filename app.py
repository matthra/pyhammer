import streamlit as st
import pandas as pd
import cpk_engine

# --- CONFIG ---
TARGETS = {
    'MEQ': {'Name': 'Marine (T4 2W 3+)', 'Pts': 18, 'T': 4, 'W': 2, 'Sv': '3+', 'Inv': ''},
    'TEQ': {'Name': 'Terminator (T5 3W 2+/4++)', 'Pts': 40, 'T': 5, 'W': 3, 'Sv': '2+', 'Inv': '4+'},
    'VEQ-H': {'Name': 'Land Raider (T12 16W 2+)', 'Pts': 240,'T': 12, 'W': 16, 'Sv': '2+', 'Inv': ''},
    'KEQ': {'Name': 'Knight (T11 22W 3+/5++)',   'Pts': 400, 'T': 11, 'W': 22, 'Sv': '3+', 'Inv': '5+'},
}

st.set_page_config(page_title="PyHammer", page_icon="⚡", layout="wide")
st.title("⚡ PyHammer")
st.markdown("""
**Cost Per Kill (CPK) Calculator**
* **Lower is better.** (e.g., 0.5 means you trade up massively. 2.0 means you trade down).
* *Math Engine licensed under AGPLv3.*
""")

# --- SIDEBAR (INPUT) ---
with st.sidebar:
    st.header("Unit Roster")
    
    # File handling
    uploaded_file = st.file_uploader("Upload Roster (.csv)", type=['csv'])
    
    if 'roster' not in st.session_state:
        # Default starter roster
        st.session_state['roster'] = pd.DataFrame([
            {'Name': 'Karnivore', 'Pts': 140, 'A': 4, 'BS': 2, 'S': 12, 'AP': -3, 'D': 'D6+2', 'Sustained':0, 'Lethal':'N', 'Dev':'N', 'RR_H':'N', 'RR_W':'N'}
        ])

    if uploaded_file:
        try:
            st.session_state['roster'] = pd.read_csv(uploaded_file)
            st.success("Roster loaded!")
        except:
            st.error("Invalid CSV format.")

    # Editable Table
    edited_df = st.data_editor(st.session_state['roster'], num_rows="dynamic")
    st.session_state['roster'] = edited_df
    
    # Download Button
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Roster (.csv)", csv, "my_roster.csv", "text/csv")

# --- MAIN (OUTPUT) ---
if not edited_df.empty:
    results = []
    for idx, row in edited_df.iterrows():
        res = {'Unit': row['Name']}
        for t_key, t_stats in TARGETS.items():
            try:
                val = cpk_engine.calculate_cpk(row, t_stats)
                res[t_key] = val
            except Exception as e:
                res[t_key] = 99.9 # Error
        results.append(res)
    
    res_df = pd.DataFrame(results).set_index('Unit')
    
    def color_scale(val):
        color = '#99ff99' if val < 1.5 else '#ffff99' if val < 2.5 else '#ff9999'
        return f'background-color: {color}; color: black'

    st.dataframe(res_df.style.map(color_scale), use_container_width=True)

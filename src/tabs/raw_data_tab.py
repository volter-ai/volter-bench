# tabs/raw_data_tab.py

import streamlit as st


def display_raw_data_tab(all_data):
    st.header("Raw Data")
    
    # Filters
    st.subheader("Filters")
    selected_ladders_raw = st.multiselect(
        "Select Ladders",
        options=sorted(all_data['ladder'].unique()),
        default=sorted(all_data['ladder'].unique()),
        key='tab4_selected_ladders'
    )
    
    selected_agents_raw = st.multiselect(
        "Select Agents",
        options=sorted(all_data['agent_id'].unique()),
        default=sorted(all_data['agent_id'].unique()),
        key='tab4_selected_agents'
    )
    
    # Filter data
    raw_filtered_data = all_data[
        (all_data['ladder'].isin(selected_ladders_raw)) &
        (all_data['agent_id'].isin(selected_agents_raw))
    ]
    
    if raw_filtered_data.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
        return
    
    st.dataframe(raw_filtered_data)


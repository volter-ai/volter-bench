# tabs/run_details_tab.py

import streamlit as st
import pandas as pd
from src.calculations import calculate_agent_ladder_success_rates
from src.github_utils import get_github_url, get_code_github_url


def display_run_details_tab(all_data, data_directory):
    st.header("Run Details")
    
    # Run selection
    selected_run = st.selectbox(
        "Select a run (Timestamp)",
        options=sorted(all_data['file_timestamp'].unique(), reverse=True),
        index=0
    )
    
    # Filter data for selected run
    run_data = all_data[all_data['file_timestamp'] == selected_run]
    
    # Success rates for selected run
    st.subheader("Agent-Ladder Success Rates for Selected Run")
    success_rates = calculate_agent_ladder_success_rates(run_data)
    st.dataframe(success_rates.style.format({
        'success_rate': '{:.2%}',
    }))
    
    # Individual run details
    st.subheader("Individual Run Details")
    run_data = run_data.copy()
    run_data['sort_key'] = (run_data['status'] == 'success').astype(int)
    sorted_run_data = run_data.sort_values(by=['sort_key', 'ladder', 'agent_id', 'run'])
    sorted_run_data = sorted_run_data.drop('sort_key', axis=1)
    
    for _, row in sorted_run_data.iterrows():
        status_icon = '❌' if row['status'] != 'success' else '✅'
        expander_title = f"{status_icon} {row['ladder']} - {row['agent_id']} (Trial {row['run']})"
        
        with st.expander(expander_title):
            st.write(f"Status: {row['status']}")
            st.write(f"Branch: {row['branch']}") 
            
            # GitHub links
            github_url = get_github_url(row, data_directory)
            st.markdown(f"[View logs on GitHub]({github_url})")
            
            github_code_url = get_code_github_url(row, data_directory)
            st.markdown(f"[View game code on GitHub]({github_code_url})")
            
            if 'commit_url' in row and pd.notna(row['commit_url']):
                st.markdown(f"[View agent code on GitHub]({row['commit_url']})")
            
            # Error and traceback display
            if row['status'] != 'success' or (pd.notna(row['error']) and str(row['error']).lower() != 'nan'):
                if pd.notna(row['error']) and str(row['error']).lower() != 'nan':
                    st.error(f"Error: {row['error']}")
                if pd.notna(row['traceback']) and str(row['traceback']).lower() != 'nan':
                    st.code(row['traceback'], language="python")

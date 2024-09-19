# tabs/run_details_tab.py

import streamlit as st
import pandas as pd
from src.calculations import calculate_agent_ladder_success_rates
from src.github_utils import get_github_url, get_code_github_url


def display_run_details_tab(all_data, data_directory):
    st.header("Run Details")

    # Select a specific run
    selected_run = st.selectbox(
        "Select a run (Timestamp)",
        options=sorted(all_data['file_timestamp'].unique(), reverse=True),
        index=0
    )

    # Filter data for the selected run
    run_data = all_data[all_data['file_timestamp'] == selected_run]

    st.subheader("Agent-Ladder Success Rates for Selected Run")
    success_rates = calculate_agent_ladder_success_rates(run_data)
    st.dataframe(success_rates.style.format({
        'success_rate': '{:.2%}',
    }))

    st.subheader("Individual Run Details")

    # Add a sorting column
    run_data = run_data.copy()
    run_data['sort_key'] = (run_data['status'] == 'success').astype(int)

    # Sort the run data
    sorted_run_data = run_data.sort_values(by=['sort_key', 'ladder', 'agent_id', 'run'])

    # Remove the sorting column
    sorted_run_data = sorted_run_data.drop('sort_key', axis=1)

    # Display runs
    for _, row in sorted_run_data.iterrows():
        status_icon = '❌' if row['status'] != 'success' else '✅'
        expander_title = f"{status_icon} {row['ladder']} - {row['agent_id']} (Trial {row['run']})"

        with st.expander(expander_title):
            st.write(f"Status: {row['status']}")

            # Generate and display GitHub links
            github_url = get_github_url(row, data_directory)
            st.markdown(f"[View logs on GitHub]({github_url})")

            # Add the "View game code on GitHub" link
            github_code_url = get_code_github_url(row, data_directory)
            st.markdown(f"[View game code on GitHub]({github_code_url})")

            # Add the "View agent code on GitHub" link using 'commit_url' from the dataframe
            if 'commit_url' in row and pd.notna(row['commit_url']):
                st.markdown(f"[View agent code on GitHub]({row['commit_url']})")

            # Only show error and traceback if they exist and aren't 'nan'
            if row['status'] != 'success' or (pd.notna(row['error']) and str(row['error']).lower() != 'nan'):
                if pd.notna(row['error']) and str(row['error']).lower() != 'nan':
                    st.error(f"Error: {row['error']}")
                if pd.notna(row['traceback']) and str(row['traceback']).lower() != 'nan':
                    st.code(row['traceback'], language="python")

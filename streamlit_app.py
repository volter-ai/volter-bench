# streamlit_app.py

import streamlit as st
import os

# Import custom modules
from src.data_loader import get_subdirectories, load_data
from src.calculations import calculate_success_rates, calculate_agent_ladder_success_rates
from src.tabs.leaderboard_tab import display_leaderboard_tab
from src.tabs.agent_performance_tab import display_agent_performance_tab
from src.tabs.run_details_tab import display_run_details_tab
from src.tabs.raw_data_tab import display_raw_data_tab


def main():
    st.set_page_config(page_title="Ladder and Agent Performance Dashboard", layout="wide")
    st.title("Run Status Dashboard")

    base_dir = "data"
    subdirs = get_subdirectories(base_dir)

    if not subdirs:
        st.error(f"No subdirectories found in the '{base_dir}' folder.")
        return

    selected_subdir = st.sidebar.selectbox(
        "Select Data Directory",
        subdirs,
        index=subdirs.index('bench_one_shot_core') if 'bench_one_shot_core' in subdirs else 0
    )
    data_directory = os.path.join(base_dir, selected_subdir)

    st.sidebar.text(f"Current directory: {data_directory}")

    all_data = load_data(data_directory)
    if all_data.empty:
        st.error(f"No CSV files found in the directory {data_directory}.")
        return

    # Identify the latest run
    latest_file_timestamp = all_data['file_timestamp'].max()
    latest_run_data = all_data[all_data['file_timestamp'] == latest_file_timestamp]

    latest_success_rates = calculate_success_rates(latest_run_data)
    latest_agent_ladder_success_rates = calculate_agent_ladder_success_rates(latest_run_data)

    if latest_success_rates.empty:
        st.warning("No success rate data available.")
    else:
        top_model = latest_success_rates.loc[latest_success_rates['success_rate'].idxmax()]

        col1, col2, col3 = st.columns(3)
        col1.metric("Top Model", top_model['agent_id'])
        col2.metric("Success Rate", f"{top_model['success_rate']:.2%}")
        col3.metric("Latest Run Timestamp", latest_file_timestamp.strftime("%Y-%m-%d %H:%M:%S"))

    tab1, tab2, tab3, tab4 = st.tabs(["Leaderboard", "Agent Performance", "Run Details", "Raw Data"])

    with tab1:
        display_leaderboard_tab(latest_success_rates, latest_agent_ladder_success_rates)

    with tab2:
        display_agent_performance_tab(all_data)

    with tab3:
        display_run_details_tab(all_data, data_directory)

    with tab4:
        display_raw_data_tab(all_data)


if __name__ == "__main__":
    main()

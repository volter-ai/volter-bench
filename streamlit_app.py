# streamlit_app.py
import streamlit as st
import os
import pandas as pd
from pathlib import Path
import logging
from src.data_loader import get_agent_types, get_branches, load_data
from src.calculations import calculate_success_rates, calculate_agent_ladder_success_rates
from src.tabs.agent_performance_tab import display_agent_performance_tab
from src.tabs.leaderboard_tab import display_leaderboard_tab
from src.tabs.raw_data_tab import display_raw_data_tab
from src.tabs.run_details_tab import display_run_details_tab
from src.visualizations import create_heatmap

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_unique_non_null_values(series: pd.Series) -> list:
    """Extract unique non-null values from a pandas series and return them sorted.
    
    Args:
        series: pandas.Series containing potentially mixed types and null values
        
    Returns:
        list: Sorted list of unique non-null values
    """
    # Convert to string, filter out null values, and get unique values
    unique_values = series.dropna().astype(str).unique().tolist()
    return sorted(unique_values)

def load_all_branch_data(base_dir, agent_type):
    """Load data from all branches for a given agent type."""
    try:
        all_branch_data = []
        branches = get_branches(base_dir, agent_type)
        
        for branch in branches:
            try:
                data_directory = os.path.join(base_dir, agent_type, branch)
                branch_data = load_data(data_directory)
                if not branch_data.empty:
                    # Add branch column if it doesn't exist
                    if 'branch' not in branch_data.columns:
                        branch_data['branch'] = branch
                    all_branch_data.append(branch_data)
            except Exception as e:
                logger.error(f"Error loading branch {branch}: {str(e)}")
        
        if not all_branch_data:
            logger.warning("No data found in any branch")
            return pd.DataFrame()
            
        return pd.concat(all_branch_data, ignore_index=True)
    except Exception as e:
        logger.error(f"Error in load_all_branch_data: {str(e)}")
        return pd.DataFrame()

def main():
    try:
        st.set_page_config(page_title="Ladder and Agent Performance Dashboard", layout="wide")
        st.title("Run Status Dashboard")
        
        base_dir = "data"
        
        # Verify data directory exists
        if not os.path.exists(base_dir):
            st.error(f"Data directory '{base_dir}' not found!")
            logger.error(f"Data directory '{base_dir}' not found!")
            return
            
        # Get available agent types
        agent_types = get_agent_types(base_dir)
        
        if not agent_types:
            st.error(f"No agent type directories found in the '{base_dir}' folder.")
            return
        
        # Agent type selection
        default_index = agent_types.index('bench_one_shot_core') if 'bench_one_shot_core' in agent_types else 0
        selected_agent_type = st.sidebar.selectbox(
            "Select Agent Type",
            agent_types,
            index=default_index
        )
        
        all_data = load_all_branch_data(base_dir, selected_agent_type)
        
        if all_data.empty:
            st.error(f"No data found for agent type '{selected_agent_type}'.")
            return
        
        # Sidebar filters
        st.sidebar.markdown("### Global Filters")
        
        # Branch filter
        available_branches = sorted(all_data['branch'].unique())
        selected_branch = st.sidebar.selectbox(
            "Select Branch",
            options=['All Branches'] + available_branches,
            index=0,
            key='global_branch_filter'
        )
        
        # Project type filter - handle null values safely
        available_project_types = (
            get_unique_non_null_values(all_data['project_type'])
            if 'project_type' in all_data.columns
            else []
        )
        
        selected_project_type = st.sidebar.selectbox(
            "Select Project Type",
            options=['All Projects'] + available_project_types,
            index=0,
            key='global_project_filter'
        )
        
        # Apply filters
        filtered_data = all_data.copy()
        if selected_branch != 'All Branches':
            filtered_data = filtered_data[filtered_data['branch'] == selected_branch]
        if selected_project_type != 'All Projects' and 'project_type' in filtered_data.columns:
            # Convert to string for comparison to handle mixed types
            filtered_data = filtered_data[
                filtered_data['project_type'].astype(str) == selected_project_type
            ]
        
        if filtered_data.empty:
            st.warning("No data available for the selected filters.")
            return
        
        # Dashboard header metrics
        latest_file_timestamp = filtered_data['file_timestamp'].max()
        latest_run_data = filtered_data[filtered_data['file_timestamp'] == latest_file_timestamp]
        latest_success_rates = calculate_success_rates(latest_run_data)
        latest_agent_ladder_success_rates = calculate_agent_ladder_success_rates(latest_run_data)
        
        if latest_success_rates.empty:
            st.warning("No success rate data available for the selected filters.")
        else:
            top_model = latest_success_rates.loc[latest_success_rates['success_rate'].idxmax()]
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Top Model", top_model['agent_id'])
            col2.metric("Success Rate", f"{top_model['success_rate']:.2%}")
            col3.metric("Branch", selected_branch)
            col4.metric("Project Type", selected_project_type)
            col5.metric("Latest Run Timestamp", latest_file_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Leaderboard", "Agent Performance", "Run Details", "Raw Data"])
        
        with tab1:
            display_leaderboard_tab(latest_success_rates, latest_agent_ladder_success_rates)
        with tab2:
            display_agent_performance_tab(filtered_data, selected_branch)
        with tab3:
            display_run_details_tab(filtered_data, os.path.join(base_dir, selected_agent_type))
        with tab4:
            display_raw_data_tab(filtered_data)
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
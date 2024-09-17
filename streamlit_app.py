import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px


def get_subdirectories(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]


def load_data(directory):
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'results.csv':
                csv_files.append(os.path.join(root, file))

    all_data = []
    for file in csv_files:
        df = pd.read_csv(file)
        # Extract timestamp from the file path
        timestamp = file.split(os.path.sep)[-2]
        df['file_timestamp'] = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S")
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()


def calculate_success_rates(df):
    success_rates = df.groupby('agent_id').agg({
        'status': lambda x: (x == 'success').mean(),
    }).reset_index()
    success_rates.columns = ['agent_id', 'success_rate']
    return success_rates


def calculate_agent_ladder_success_rates(df):
    success_rates = df.groupby(['agent_id', 'ladder']).agg({
        'status': lambda x: (x == 'success').mean(),
    }).reset_index()
    success_rates.columns = ['agent_id', 'ladder', 'success_rate']
    return success_rates


def create_heatmap(data, value_column, title):
    heatmap_pivot = data.pivot(index='ladder', columns='agent_id', values=value_column)

    fig = px.imshow(heatmap_pivot,
                    labels=dict(x="Agent ID", y="Ladder", color="Success Rate"),
                    x=heatmap_pivot.columns,
                    y=heatmap_pivot.index,
                    color_continuous_scale=['red', 'yellow', 'green'],
                    zmin=0, zmax=1)
    fig.update_layout(title=title)
    return fig


def get_github_url(row):
    base_url = "https://github.com/volter-ai/volter-bench/tree/main/data/bench_one_shot_view"

    # Format the timestamp to match the GitHub folder structure
    formatted_timestamp = row['file_timestamp'].strftime("%Y-%m-%d-%H-%M-%S")

    # Extract the log file name from the logs path and remove any extra characters
    log_path = row['logs'][0] if isinstance(row['logs'], list) else row['logs']
    log_file = log_path.split('/')[-1].strip("[]'")

    # Construct the GitHub URL
    github_url = f"{base_url}/{formatted_timestamp}/new_prompt_logs/{log_file}"

    return github_url


def main():
    st.set_page_config(page_title="Ladder and Agent Performance Dashboard", layout="wide")
    st.title("Run Status Dashboard")

    base_dir = "data"
    subdirs = get_subdirectories(base_dir)

    if not subdirs:
        st.error(f"No subdirectories found in the '{base_dir}' folder.")
        return

    selected_subdir = st.sidebar.selectbox("Select Data Directory", subdirs,
                                           index=subdirs.index(
                                               'bench_one_shot_core') if 'bench_one_shot_core' in subdirs else 0)
    data_directory = os.path.join(base_dir, selected_subdir)

    st.sidebar.text(f"Current directory: {data_directory}")

    all_data = load_data(data_directory)
    if all_data.empty:
        st.error(f"No CSV files found in the directory {data_directory}.")
        return

    # Filters
    st.sidebar.header("Filters")
    selected_timestamps = st.sidebar.multiselect(
        "Select Run Timestamps",
        options=sorted(all_data['file_timestamp'].unique(), reverse=True),
        default=sorted(all_data['file_timestamp'].unique(), reverse=True)
    )
    selected_ladders = st.sidebar.multiselect(
        "Select Ladders",
        options=sorted(all_data['ladder'].unique()),
        default=sorted(all_data['ladder'].unique())
    )
    selected_agents = st.sidebar.multiselect(
        "Select Agents",
        options=sorted(all_data['agent_id'].unique()),
        default=sorted(all_data['agent_id'].unique())
    )

    # Filter data based on selections
    filtered_data = all_data[
        (all_data['file_timestamp'].isin(selected_timestamps)) &
        (all_data['ladder'].isin(selected_ladders)) &
        (all_data['agent_id'].isin(selected_agents))
        ]

    if filtered_data.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
        return

    latest_file_timestamp = filtered_data['file_timestamp'].max()
    latest_run_data = filtered_data[filtered_data['file_timestamp'] == latest_file_timestamp]

    latest_success_rates = calculate_success_rates(latest_run_data)
    latest_agent_ladder_success_rates = calculate_agent_ladder_success_rates(latest_run_data)

    if latest_success_rates.empty:
        st.warning("No success rate data available for the selected filters. Please adjust your selection.")
    else:
        top_model = latest_success_rates.loc[latest_success_rates['success_rate'].idxmax()]

        col1, col2, col3 = st.columns(3)
        col1.metric("Top Model", top_model['agent_id'])
        col2.metric("Success Rate", f"{top_model['success_rate']:.2%}")
        col3.metric("Latest Run Timestamp", latest_file_timestamp.strftime("%Y-%m-%d %H:%M:%S"))

    tab1, tab2, tab3, tab4 = st.tabs(["Leaderboard", "Agent Performance", "Run Details", "Raw Data"])

    with tab1:
        st.header("Leaderboard (Latest Run)")

        if latest_success_rates.empty:
            st.warning("No data available for the leaderboard. Please adjust your filter selection.")
        else:
            st.dataframe(latest_success_rates.sort_values('success_rate', ascending=False).style.format({
                'success_rate': '{:.2%}',
            }))

            st.subheader("Agent-Ladder Success Rate Grid (Latest Run)")
            heatmap_fig = create_heatmap(latest_agent_ladder_success_rates, 'success_rate',
                                         "Success Rate Grid (Latest Run)")
            st.plotly_chart(heatmap_fig)

    with tab2:
        st.header("Agent Performance Over Time")

        fig = go.Figure()
        for agent in filtered_data['agent_id'].unique():
            agent_data = filtered_data[filtered_data['agent_id'] == agent].groupby('file_timestamp').agg({
                'status': lambda x: (x == 'success').mean() * 100  # Convert to percentage
            }).reset_index()
            fig.add_trace(go.Scatter(x=agent_data['file_timestamp'],
                                     y=agent_data['status'],
                                     mode='lines+markers',
                                     name=agent))

        fig.update_layout(title="Success Rate Over Time",
                          xaxis_title="Timestamp",
                          yaxis_title="Success Rate (%)",
                          yaxis=dict(range=[0, 100]))  # Set y-axis range from 0 to 100
        st.plotly_chart(fig)

        # Add a data table showing the success rates
        st.subheader("Success Rates Table")
        success_rates = filtered_data.groupby(['file_timestamp', 'agent_id', 'ladder']).agg({
            'status': lambda x: (x == 'success').mean() * 100  # Convert to percentage
        }).reset_index()
        success_rates.columns = ['Timestamp', 'Agent', 'Ladder', 'Success Rate (%)']
        success_rates = success_rates.sort_values(['Timestamp', 'Ladder', 'Agent'], ascending=[False, True, True])
        st.dataframe(success_rates.style.format({'Success Rate (%)': '{:.2f}'}))

        # Add a summary table for overall performance
        st.subheader("Overall Performance Summary")
        overall_performance = filtered_data.groupby('agent_id').agg({
            'status': lambda x: (x == 'success').mean() * 100  # Convert to percentage
        }).reset_index()
        overall_performance.columns = ['Agent', 'Overall Success Rate (%)']
        overall_performance = overall_performance.sort_values('Overall Success Rate (%)', ascending=False)
        st.dataframe(overall_performance.style.format({'Overall Success Rate (%)': '{:.2f}'}))

    with tab3:
        st.header("Run Details")

        st.subheader("Agent-Ladder Success Rates for Selected Runs")
        success_rates = calculate_agent_ladder_success_rates(filtered_data)
        st.dataframe(success_rates.style.format({
            'success_rate': '{:.2%}',
        }))

        st.subheader("Individual Run Details")

        # Add a sorting column
        filtered_data['sort_key'] = (filtered_data['status'] == 'success').astype(int)

        # Sort the run data
        sorted_run_data = filtered_data.sort_values(by=['sort_key', 'ladder', 'agent_id', 'run'])

        # Remove the sorting column
        sorted_run_data = sorted_run_data.drop('sort_key', axis=1)

        # Display runs
        for _, row in sorted_run_data.iterrows():
            status_icon = '❌' if row['status'] != 'success' else '✅'
            expander_title = f"{status_icon} {row['ladder']} - {row['agent_id']} (Trial {row['run']}) - {row['file_timestamp']}"

            with st.expander(expander_title):
                st.write(f"Status: {row['status']}")

                # Generate and display GitHub link
                github_url = get_github_url(row)
                st.markdown(f"[View logs on GitHub]({github_url})")

                # Only show error and traceback if they exist and aren't 'nan'
                if row['status'] != 'success' or (pd.notna(row['error']) and str(row['error']).lower() != 'nan'):
                    if pd.notna(row['error']) and str(row['error']).lower() != 'nan':
                        st.error(f"Error: {row['error']}")
                    if pd.notna(row['traceback']) and str(row['traceback']).lower() != 'nan':
                        st.code(row['traceback'], language="python")

    with tab4:
        st.header("Raw Data")
        st.dataframe(filtered_data)


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
from datetime import datetime
import plotly.express as px


def get_subdirectories(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]


def load_data(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    all_data = []
    for file in csv_files:
        df = pd.read_csv(os.path.join(directory, file))
        df['file_timestamp'] = datetime.strptime(file.split('_')[-1].split('.')[0], "%Y-%m-%d-%H-%M-%S")
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


def main():
    st.set_page_config(page_title="Ladder and Agent Performance Dashboard", layout="wide")
    st.title("Run Status Dashboard")

    base_dir = "data"
    subdirs = get_subdirectories(base_dir)

    if not subdirs:
        st.error(f"No subdirectories found in the '{base_dir}' folder.")
        return

    selected_subdir = st.sidebar.selectbox("Select Data Directory", subdirs,
                                           index=subdirs.index('bench_one_shot_core') if 'bench_one_shot_core' in subdirs else 0)
    data_directory = os.path.join(base_dir, selected_subdir)

    st.sidebar.text(f"Current directory: {data_directory}")

    all_data = load_data(data_directory)
    if all_data.empty:
        st.error(f"No CSV files found in the directory {data_directory}.")
        return

    latest_file_timestamp = all_data['file_timestamp'].max()
    latest_run_data = all_data[all_data['file_timestamp'] == latest_file_timestamp]

    latest_success_rates = calculate_success_rates(latest_run_data)
    latest_agent_ladder_success_rates = calculate_agent_ladder_success_rates(latest_run_data)

    top_model = latest_success_rates.loc[latest_success_rates['success_rate'].idxmax()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Top Model", top_model['agent_id'])
    col2.metric("Success Rate", f"{top_model['success_rate']:.2%}")
    col3.metric("Latest Run Timestamp", latest_file_timestamp.strftime("%Y-%m-%d %H:%M:%S"))

    tab1, tab2, tab3, tab4 = st.tabs(["Leaderboard", "Agent Performance", "Run Details", "Raw Data"])

    with tab1:
        st.header("Leaderboard (Latest Run)")

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
        for agent in all_data['agent_id'].unique():
            agent_data = all_data[all_data['agent_id'] == agent].groupby('file_timestamp').agg({
                'status': lambda x: (x == 'success').mean()
            }).reset_index()
            fig.add_trace(go.Scatter(x=agent_data['file_timestamp'],
                                     y=agent_data['status'],
                                     mode='lines+markers',
                                     name=agent))

        fig.update_layout(title="Success Rate Over Time",
                          xaxis_title="Timestamp",
                          yaxis_title="Success Rate")
        st.plotly_chart(fig)

    with tab3:
        st.header("Run Details")
        file_timestamps = sorted(all_data['file_timestamp'].unique(), reverse=True)
        selected_timestamp = st.selectbox("Select a run (Timestamp)", file_timestamps)

        run_data = all_data[all_data['file_timestamp'] == selected_timestamp]

        st.subheader("Agent-Ladder Success Rates for Selected Run")
        success_rates = calculate_agent_ladder_success_rates(run_data)
        st.dataframe(success_rates.style.format({
            'success_rate': '{:.2%}',
        }))

        st.subheader("Individual Run Details")

        # Sort the run data by status (success first, then failure)
        sorted_run_data = run_data.sort_values(by=['status', 'ladder', 'agent_id'],
                                               ascending=[False, True, True])

        # Group runs by ladder and agent
        grouped_runs = sorted_run_data.groupby(['ladder', 'agent_id'])

        for (ladder, agent_id), group in grouped_runs:
            for i, (_, row) in enumerate(group.iterrows(), 1):
                status_icon = '✅' if row['status'] == 'success' else '❌'
                expander_title = f"{status_icon} {ladder} - {agent_id} (Trial {i})"

                with st.expander(expander_title):
                    st.write(f"Status: {row['status']}")
                    if row['error']:
                        st.error(f"Error: {row['error']}")
                    if row['traceback']:
                        st.code(row['traceback'], language="python")

    with tab4:
        st.header("Raw Data")
        st.dataframe(all_data)


if __name__ == "__main__":
    main()
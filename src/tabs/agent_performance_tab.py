# tabs/agent_performance_tab.py

import streamlit as st
import plotly.graph_objects as go


def display_agent_performance_tab(all_data):
    st.header("Agent Performance Over Time")

    # Filters specific to this tab
    st.subheader("Filters")
    selected_ladders = st.multiselect(
        "Select Ladders",
        options=sorted(all_data['ladder'].unique()),
        default=sorted(all_data['ladder'].unique()),
        key='tab2_selected_ladders'
    )
    selected_agents = st.multiselect(
        "Select Agents",
        options=sorted(all_data['agent_id'].unique()),
        default=sorted(all_data['agent_id'].unique()),
        key='tab2_selected_agents'
    )

    # Filter data based on selections
    filtered_data = all_data[
        (all_data['ladder'].isin(selected_ladders)) &
        (all_data['agent_id'].isin(selected_agents))
        ]

    if filtered_data.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
        return

    fig = go.Figure()
    for agent in filtered_data['agent_id'].unique():
        agent_data = filtered_data[filtered_data['agent_id'] == agent].groupby('file_timestamp').agg({
            'status': lambda x: (x == 'success').mean() * 100  # Convert to percentage
        }).reset_index()
        fig.add_trace(go.Scatter(
            x=agent_data['file_timestamp'],
            y=agent_data['status'],
            mode='lines+markers',
            name=agent
        ))

    fig.update_layout(
        title="Success Rate Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Success Rate (%)",
        yaxis=dict(range=[0, 100]),
        margin=dict(t=80)
    )
    st.plotly_chart(fig)

    # Add a data table showing the success rates
    st.subheader("Success Rates Table")
    success_rates = filtered_data.groupby(['file_timestamp', 'agent_id', 'ladder']).agg({
        'status': lambda x: (x == 'success').mean() * 100
    }).reset_index()
    success_rates.columns = ['Timestamp', 'Agent', 'Ladder', 'Success Rate (%)']
    success_rates = success_rates.sort_values(['Timestamp', 'Ladder', 'Agent'], ascending=[False, True, True])
    st.dataframe(success_rates.style.format({'Success Rate (%)': '{:.2f}'}))

    # Add a summary table for overall performance
    st.subheader("Overall Performance Summary")
    overall_performance = filtered_data.groupby('agent_id').agg({
        'status': lambda x: (x == 'success').mean() * 100
    }).reset_index()
    overall_performance.columns = ['Agent', 'Overall Success Rate (%)']
    overall_performance = overall_performance.sort_values('Overall Success Rate (%)', ascending=False)
    st.dataframe(overall_performance.style.format({'Overall Success Rate (%)': '{:.2f}'}))

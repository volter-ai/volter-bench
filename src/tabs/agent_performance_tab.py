# tabs/agent_performance_tab.py

import streamlit as st
import plotly.graph_objects as go


def display_agent_performance_tab(filtered_data, selected_branch):
    st.header("Agent Performance Over Time")
    branch_text = f"({selected_branch})" if selected_branch != 'All Branches' else "(All Branches)"
    st.subheader(f"Performance Trends {branch_text}")
    
    # Filters
    st.subheader("Filters")
    selected_ladders = st.multiselect(
        "Select Ladders",
        options=sorted(filtered_data['ladder'].unique()),
        default=sorted(filtered_data['ladder'].unique()),
        key='tab2_selected_ladders'
    )
    
    selected_agents = st.multiselect(
        "Select Agents",
        options=sorted(filtered_data['agent_id'].unique()),
        default=sorted(filtered_data['agent_id'].unique()),
        key='tab2_selected_agents'
    )
    
    # Filter data
    tab_filtered_data = filtered_data[
        (filtered_data['ladder'].isin(selected_ladders)) &
        (filtered_data['agent_id'].isin(selected_agents))
    ]
    
    if tab_filtered_data.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
        return
    
    # Success rate over time plot
    fig = go.Figure()
    for agent in tab_filtered_data['agent_id'].unique():
        agent_data = tab_filtered_data[tab_filtered_data['agent_id'] == agent].groupby(['file_timestamp', 'branch']).agg({
            'status': lambda x: (x == 'success').mean() * 100
        }).reset_index()
        
        # Add branch information to hover text if showing all branches
        if selected_branch == 'All Branches':
            hover_text = [f"Branch: {branch}" for branch in agent_data['branch']]
        else:
            hover_text = None
        
        fig.add_trace(go.Scatter(
            x=agent_data['file_timestamp'],
            y=agent_data['status'],
            mode='lines+markers',
            name=agent,
            text=hover_text,
            hovertemplate="%{text}<br>Success Rate: %{y:.1f}%<br>%{x}" if hover_text else None
        ))
    
    fig.update_layout(
        title=f"Success Rate Over Time {branch_text}",
        xaxis_title="Timestamp",
        yaxis_title="Success Rate (%)",
        yaxis=dict(range=[0, 100]),
        margin=dict(t=80)
    )
    st.plotly_chart(fig)
    
    # Success rates table
    st.subheader(f"Success Rates Table {branch_text}")
    groupby_cols = ['file_timestamp', 'agent_id', 'ladder']
    if selected_branch == 'All Branches':
        groupby_cols.append('branch')
    
    success_rates = tab_filtered_data.groupby(groupby_cols).agg({
        'status': lambda x: (x == 'success').mean() * 100
    }).reset_index()
    
    # Rename columns based on whether branch is included
    if selected_branch == 'All Branches':
        success_rates.columns = ['Timestamp', 'Agent', 'Ladder', 'Branch', 'Success Rate (%)']
        sort_cols = ['Timestamp', 'Branch', 'Ladder', 'Agent']
    else:
        success_rates.columns = ['Timestamp', 'Agent', 'Ladder', 'Success Rate (%)']
        sort_cols = ['Timestamp', 'Ladder', 'Agent']
    
    success_rates = success_rates.sort_values(sort_cols, ascending=[False] + [True] * (len(sort_cols) - 1))
    st.dataframe(success_rates.style.format({'Success Rate (%)': '{:.2f}'}))
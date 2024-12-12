import streamlit as st
import plotly.graph_objects as go

def create_success_rate_figure(tab_filtered_data, selected_branch, branch_text):
    fig = go.Figure()
    
    for agent in tab_filtered_data['agent_id'].unique():
        agent_data = tab_filtered_data[tab_filtered_data['agent_id'] == agent].groupby(['file_timestamp', 'branch']).agg({
            'status': lambda x: (x == 'success').mean() * 100
        }).reset_index()
        
        hover_text = [f"Branch: {branch}" for branch in agent_data['branch']] if selected_branch == 'All Branches' else None
        
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
        margin=dict(t=80),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )
    return fig

def create_duration_figure(tab_filtered_data, selected_branch, branch_text):
    fig = go.Figure()
    
    for agent in tab_filtered_data['agent_id'].unique():
        agent_data = tab_filtered_data[tab_filtered_data['agent_id'] == agent].groupby(['file_timestamp', 'branch']).agg({
            'duration': 'mean'
        }).reset_index()
        
        if 'duration' in agent_data.columns and not agent_data['duration'].isna().all():
            hover_text = [f"Branch: {branch}" for branch in agent_data['branch']] if selected_branch == 'All Branches' else None
            
            fig.add_trace(go.Scatter(
                x=agent_data['file_timestamp'],
                y=agent_data['duration'],
                mode='lines+markers',
                name=agent,
                marker=dict(symbol='diamond'),
                text=hover_text,
                hovertemplate="%{text}<br>Duration: %{y:.2f}s<br>%{x}" if hover_text else "Duration: %{y:.2f}s<br>%{x}"
            ))
    
    fig.update_layout(
        title=f"Run Duration Over Time {branch_text}",
        xaxis_title="Timestamp",
        yaxis_title="Duration (seconds)",
        margin=dict(t=80),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )
    return fig

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
    
    # Create and display success rate figure
    success_fig = create_success_rate_figure(tab_filtered_data, selected_branch, branch_text)
    st.plotly_chart(success_fig, use_container_width=True)
    
    # Create and display duration figure if duration data exists
    if 'duration' in tab_filtered_data.columns and not tab_filtered_data['duration'].isna().all():
        duration_fig = create_duration_figure(tab_filtered_data, selected_branch, branch_text)
        st.plotly_chart(duration_fig, use_container_width=True)
    
    # Success rates table
    st.subheader(f"Success Rates Table {branch_text}")
    groupby_cols = ['file_timestamp', 'agent_id', 'ladder']
    if selected_branch == 'All Branches':
        groupby_cols.append('branch')
    
    # Add duration to the aggregation if it exists
    agg_dict = {'status': lambda x: (x == 'success').mean() * 100}
    if 'duration' in tab_filtered_data.columns:
        agg_dict['duration'] = 'mean'
    
    success_rates = tab_filtered_data.groupby(groupby_cols).agg(agg_dict).reset_index()
    
    # Rename columns based on whether branch is included
    if selected_branch == 'All Branches':
        base_cols = ['Timestamp', 'Agent', 'Ladder', 'Branch']
    else:
        base_cols = ['Timestamp', 'Agent', 'Ladder']
    
    # Rename all columns including duration if it exists
    new_cols = base_cols + ['Success Rate (%)']
    if 'duration' in success_rates.columns:
        new_cols.append('Duration (s)')
    success_rates.columns = new_cols
    
    # Sort columns
    sort_cols = base_cols[:-1]  # Exclude the last base column for sorting
    success_rates = success_rates.sort_values(sort_cols, ascending=[False] + [True] * (len(sort_cols) - 1))
    
    # Format numeric columns
    format_dict = {'Success Rate (%)': '{:.2f}'}
    if 'Duration (s)' in success_rates.columns:
        format_dict['Duration (s)'] = '{:.2f}'
    
    st.dataframe(success_rates.style.format(format_dict))
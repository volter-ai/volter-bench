# tabs/leaderboard_tab.py

import streamlit as st
from src.visualizations import create_heatmap


def display_leaderboard_tab(latest_success_rates, latest_agent_ladder_success_rates):
    st.header("Leaderboard (Latest Run)")

    if latest_success_rates.empty:
        st.warning("No data available for the leaderboard.")
    else:
        st.dataframe(latest_success_rates.sort_values('success_rate', ascending=False).style.format({
            'success_rate': '{:.2%}',
        }))

        st.subheader("Agent-Ladder Success Rate Grid (Latest Run)")
        heatmap_fig = create_heatmap(
            latest_agent_ladder_success_rates,
            'success_rate',
            "Success Rate Grid (Latest Run)"
        )
        st.plotly_chart(heatmap_fig)

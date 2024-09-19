# visualizations.py

import plotly.express as px


def create_heatmap(data, value_column, title):
    heatmap_pivot = data.pivot(index='ladder', columns='agent_id', values=value_column)

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Agent ID", y="Ladder", color="Success Rate"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale=['red', 'yellow', 'green'],
        zmin=0,
        zmax=1,
    )
    fig.update_layout(title=title)
    return fig

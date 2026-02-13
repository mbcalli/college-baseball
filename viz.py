import plotly.graph_objects as go
import pandas as pd

# Input data
df = pd.read_csv("data_transposed.csv")

# Sort so y-axis is stable (optional)
df = df.sort_values('2025')

# Create figure
fig = go.Figure()

# Add lines and arrows
for idx, row in df.iterrows():
    x0 = row['2025']
    x1 = row['2026']
    y = row['Team']
    color = 'blue' if x1 < x0 else 'red'

    # Line
    fig.add_trace(go.Scatter(
        x=[x0, x1], y=[y, y],
        # mode='lines+markers',
        mode="lines",
        line=dict(color=color, width=3),
        showlegend=False
    ))

    # Arrow head
    fig.add_annotation(
        x=x1, y=y,
        ax=x0, ay=y,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=5,
        arrowsize=1,
        arrowwidth=5,
        arrowcolor=color
    )

# Formatting
fig.update_layout(
    title="Effect of Pick Ups and Losses (lower is better)",
    xaxis_title="Rank (lower is better)",
    yaxis_title="Stat",
    xaxis=dict(autorange='reversed', showgrid=True),
    template='plotly_white',
    height=400,
    width=600
)

fig.show()
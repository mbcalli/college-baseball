import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def perc_to_color(value):
    val = max(0, min(100, value))  # clamp to [0, 100]
    r = int(255 * (val / 100))        # red increases
    g = 0                             # keep green constant
    b = int(255 * (1 - val / 100))    # blue decreases
    return f'#{r:02x}{g:02x}{b:02x}'

def perc_to_pastel_color(value, desaturation=0.1):
    val = max(0, min(100, value))  # clamp to [0, 100]
    r = int(255 * (val / 100))
    g = 0
    b = int(255 * (1 - val / 100))

    # Blend with white (255, 255, 255)
    r = int(r + (255 - r) * desaturation)
    g = int(g + (255 - g) * desaturation)
    b = int(b + (255 - b) * desaturation)

    return f'#{r:02x}{g:02x}{b:02x}'

def value_to_string(value):
    if value > 10: return f"{value:0.0f}"
    if value > 5: return f"{value:0.1f}"
    if value > 1: return f"{value:0.2f}"
    return f"{value:0.3f}"

def get_player_df(player_name: str) -> pd.DataFrame:

    player_processed = processed_batting[processed_batting["name"] == player_name]
    player_processed = player_processed.drop(columns=["id", "name", "team"]).T.reset_index()
    player_processed.columns = ["stat", "perc"]
    player_processed["stat"] = [
        "PA",
        "BB%",
        "K%",
        "BB/K",
        "AVG",
        "OBP",
        "SLG",
        "OPS",
        "ISO",
        "Spd",
        "BABIP",
        "wSB",
        "wRC",
        "wRAA",
        "wOBA",
        "wRC+"
    ]

    player_raw = raw_batting[raw_batting["name"] == player_name]
    player_raw = player_raw.drop(columns=["id", "name", "team", "age", "alt_name"]).T.reset_index()
    player_raw.columns = ["stat", "value"]
    player_raw["stat"] = [
        "PA",
        "BB%",
        "K%",
        "BB/K",
        "AVG",
        "OBP",
        "SLG",
        "OPS",
        "ISO",
        "Spd",
        "BABIP",
        "wSB",
        "wRC",
        "wRAA",
        "wOBA",
        "wRC+"
    ]

    player_df = pd.merge(left=player_processed, right=player_raw, on="stat")


    # player_df["color"] = player_df["perc"].apply(perc_to_color)
    player_df["color"] = player_df["perc"].apply(perc_to_pastel_color)
    player_df["value_str"] = player_df["value"].apply(value_to_string)
    player_df = player_df.iloc[::-1]

    return player_df

def get_player_batting_figure(player_name: str):

    player_df = get_player_df(player_name)

    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.8, 0.2],
        shared_yaxes=True,
        horizontal_spacing=0
    )

    # Background bar (100% reference)
    fig.add_trace(
        go.Bar(
            x=[100] * len(player_df),
            y=player_df["stat"],
            orientation="h",
            marker_color="lightgray",
            opacity=0.3,
            showlegend=False,
            hoverinfo="skip"
        ),
        row=1, col=1
    )

    # Foreground bar (actual values)
    fig.add_trace(
        go.Bar(
            x=player_df["perc"],
            y=player_df["stat"],
            orientation="h",
            marker_color=player_df["color"],
            text=player_df["perc"],
            textposition="inside",
            textangle=0,
            showlegend=False,
            hoverinfo="skip"
        ),
        row=1, col=1
    )

    # Absolute Stats
    fig.add_trace(
        go.Scatter(
            x=[0] * len(player_df),
            y=player_df["stat"],
            mode="text",
            text=player_df["value_str"],  # replace with your column
            textposition="middle right",
            textfont=dict(color="black", size=10),
            showlegend=False,
            hoverinfo="skip"
        ),
        row=1, col=2
    )

    fig.update_layout(
        width=600,
        height=600,
        barmode="overlay",
        plot_bgcolor="white",
        paper_bgcolor="white",
        # margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            visible=False
        ),
        yaxis=dict(
            showgrid=False
        ),
        xaxis2=dict(
            range=[0,1],
            visible=False
        ),
        yaxis2=dict(
            showgrid=False
        ),
        title=f"Batting - {player_name}"
    )

    return fig

st.write("Batting Statistic Percentiles")

player_name = st.selectbox(
    "Batter",
    [
        "Cam Cannarella", 
        "Dom Listi", 
        "Josh Paino", 
        "Jarren Purify", 
        "Collin Priest", 
        "Andrew Ciufo", 
        "Jacob Jarrell",
        "Luke Gaffney",
        "Jack Crighton",
        "Tryston McCladdie",
        "Tristan Bissetta",
        "TP Wentworth"
    ]
)

if st.button("Show"):
    connection = sqlite3.connect("src/college_baseball/baseball.db")
    raw_batting = pd.read_sql(f"SELECT * FROM raw_batting WHERE name = '{player_name}'", connection)
    processed_batting = pd.read_sql(f"SELECT * FROM processed_batting WHERE name = '{player_name}'", connection)
    connection.close()

    fig = get_player_batting_figure(player_name)

    st.plotly_chart(fig)
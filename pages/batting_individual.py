import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json

with open("static/batters.json", "r") as file:
    batters = json.load(file)

st.title("2025 College Baseball Batting Stats")

team_name = st.selectbox(
    "Team",
    list(batters.keys()),
    index=list(batters.keys()).index("CLEM"),
    key="batting_team_ind"
)

batter_name = st.selectbox(
    "Batter",
    batters[team_name],
    key="batter"
)

if st.button("Show", key="batting_show_ind"):
    connection = sqlite3.connect("baseball.db")
    bronze_adv_batting = pd.read_sql(f"SELECT * FROM bronze_adv_batting WHERE name = '{batter_name}'", connection)
    silver_adv_batting = pd.read_sql(f"SELECT * FROM silver_adv_batting WHERE name = '{batter_name}'", connection)
    connection.close()

    fig = get_player_batting_figure(batter_name, silver_adv_batting, bronze_adv_batting)

    st.plotly_chart(fig, config={"staticPlot": True})

    st.caption("National percentiles shown within bars. 99 corresponds to the 99th percentile (GREAT)")

    with open("static/batting_metrics.json", "r") as file:
        metrics = json.load(file)

    df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Description"])
    st.dataframe(df, use_container_width=True, hide_index=True)
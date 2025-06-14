import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json


with open("static/batters.json", "r") as file:
    batters = json.load(file)

st.title("2025 Team Lineup")

st.info("Tap the ▶️ in the top-left to navigate to other pages")

team_name = st.selectbox(
    "Team",
    list(batters.keys()),
    index=list(batters.keys()).index("CLEM"),
    key="batting_team_team"
)

with open("static/batting_metrics_map.json", "r") as file:
    batting_metrics = json.load(file)

stat_name = st.selectbox(
    "Statistic",
    list(batting_metrics.keys()),
    index=list(batting_metrics.keys()).index("AVG"),
    key="batting_stat"
)

min_pa = st.selectbox(
    "Minimum PA",
    options=[0, 50, 100, 150, 200],
    index=2
)

if st.button("Show", key="batting_show_team"):

    fig = get_team_stat_batting_fig(team_name, batting_metrics[stat_name], stat_name, min_pa=min_pa)

    st.plotly_chart(fig, config={"staticPlot": True})

    st.caption("National percentiles shown within bars. 99 corresponds to the 99th percentile (GREAT)")
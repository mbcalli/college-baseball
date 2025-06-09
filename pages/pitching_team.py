import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json

with open("static/pitchers.json", "r") as file:
    pitchers = json.load(file)

st.title("2025 Team Bullpen")

st.info("Tap the ▶️ in the top-left to navigate to other pages")

team_name = st.selectbox(
    "Team",
    list(pitchers.keys()),
    index=list(pitchers.keys()).index("CLEM"),
    key="pitching_team_team"
)

with open("static/pitching_metrics_map.json", "r") as file:
    pitching_metrics = json.load(file)

stat_name = st.selectbox(
    "Statistic",
    list(pitching_metrics.keys()),
    index=list(pitching_metrics.keys()).index("ERA"),
    key="pitching_stat"
)

min_ip = st.selectbox(
    "Minimum IP",
    options=[0, 10, 20, 30, 50],
    index=2
)

if st.button("Show", key="pitching_show_team"):

    fig = get_team_stat_pitching_fig(team_name, pitching_metrics[stat_name], stat_name, min_ip=min_ip)

    st.plotly_chart(fig, config={"staticPlot": True})

    st.caption("National percentiles shown within bars. 99 corresponds to the 99th percentile (GREAT)")
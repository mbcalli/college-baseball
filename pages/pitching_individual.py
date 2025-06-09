import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json

with open("static/pitchers.json", "r") as file:
    pitchers = json.load(file)
    
st.title("2025 Individual Pitching")

st.info("Tap the ▶️ in the top-left to navigate to other pages")

team_name = st.selectbox(
    "Team",
    list(pitchers.keys()),
    index=list(pitchers.keys()).index("CLEM"),
    key="pitching_team_ind"
)

pitcher_name = st.selectbox(
    "Pitcher",
    pitchers[team_name],
    key="pitcher"
)

use_advanced = st.toggle("Advanced Stats", value=True)

if st.button("Show", key="pitching_show_ind"):
    connection = sqlite3.connect("baseball.db")
    if use_advanced:
        bronze = pd.read_sql(f"SELECT * FROM bronze_adv_pitching WHERE name = '{pitcher_name}'", connection)
        silver = pd.read_sql(f"SELECT * FROM silver_adv_pitching WHERE name = '{pitcher_name}'", connection)
    else:
        bronze = pd.read_sql(f"SELECT * FROM bronze_std_pitching WHERE name = '{pitcher_name}'", connection)
        silver = pd.read_sql(f"SELECT * FROM silver_std_pitching WHERE name = '{pitcher_name}'", connection)
    connection.close()

    fig = get_player_pitching_figure(pitcher_name, silver, bronze, use_advanced)

    st.plotly_chart(fig, config={"staticPlot": True})

    st.caption("National percentiles shown within bars. 99 corresponds to the 99th percentile (GREAT)")

    if use_advanced:
        with open("static/pitching_adv_metrics.json", "r") as file:
            metrics = json.load(file)
    else:
        with open("static/pitching_std_metrics.json", "r") as file:
            metrics = json.load(file)

    df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Description"])
    st.dataframe(df, use_container_width=True, hide_index=True)

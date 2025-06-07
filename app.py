import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json

batting_tab, pitching_tab = st.tabs(["Batting", "Pitching"])

with batting_tab:
    with open("batters.json", "r") as file:
        batters = json.load(file)

    st.title("2025 College Baseball Batting Stats")

    team_name = st.selectbox(
        "Team",
        list(batters.keys()),
        index=list(batters.keys()).index("CLEM"),
        key="batting_team"
    )

    batter_name = st.selectbox(
        "Batter",
        batters[team_name],
        key="batter"
    )

    if st.button("Show", key="batting_show"):
        connection = sqlite3.connect("baseball.db")
        raw_batting = pd.read_sql(f"SELECT * FROM raw_batting WHERE name = '{batter_name}'", connection)
        processed_batting = pd.read_sql(f"SELECT * FROM processed_batting WHERE name = '{batter_name}'", connection)
        connection.close()

        fig = get_player_batting_figure(batter_name, processed_batting, raw_batting)

        st.plotly_chart(fig)

        with open("batting_metrics.json", "r") as file:
            metrics = json.load(file)

        df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Description"])
        st.dataframe(df, use_container_width=True, hide_index=True)

with pitching_tab:
    with open("pitchers.json", "r") as file:
        pitchers = json.load(file)

    st.title("2025 College Baseball Pitching Stats")

    team_name = st.selectbox(
        "Team",
        list(pitchers.keys()),
        index=list(pitchers.keys()).index("CLEM"),
        key="pitching_team"
    )

    pitcher_name = st.selectbox(
        "Pitcher",
        pitchers[team_name],
        key="pitcher"
    )

    if st.button("Show", key="pitching_show"):
        connection = sqlite3.connect("baseball.db")
        raw_pitching = pd.read_sql(f"SELECT * FROM raw_pitching WHERE name = '{pitcher_name}'", connection)
        processed_pitching = pd.read_sql(f"SELECT * FROM processed_pitching WHERE name = '{pitcher_name}'", connection)
        connection.close()

        fig = get_player_pitching_figure(pitcher_name, processed_pitching, raw_pitching)

        st.plotly_chart(fig)

        with open("pitching_metrics.json", "r") as file:
            metrics = json.load(file)

        df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Description"])
        st.dataframe(df, use_container_width=True, hide_index=True)
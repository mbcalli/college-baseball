import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json

batting_inv_tab, pitching_inv_tab, batting_team_tab, pitching_team_tab = st.tabs(["Batting - Individual", "Pitching - Individual", "Batting - Team", "Pitching - Team"])

with batting_inv_tab:
    with open("batters.json", "r") as file:
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
        raw_batting = pd.read_sql(f"SELECT * FROM raw_batting WHERE name = '{batter_name}'", connection)
        processed_batting = pd.read_sql(f"SELECT * FROM processed_batting WHERE name = '{batter_name}'", connection)
        connection.close()

        fig = get_player_batting_figure(batter_name, processed_batting, raw_batting)

        st.plotly_chart(fig)

        with open("batting_metrics.json", "r") as file:
            metrics = json.load(file)

        df = pd.DataFrame(list(metrics.items()), columns=["Metric", "Description"])
        st.dataframe(df, use_container_width=True, hide_index=True)

with pitching_inv_tab:
    with open("pitchers.json", "r") as file:
        pitchers = json.load(file)

    st.title("2025 College Baseball Pitching Stats")

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

    if st.button("Show", key="pitching_show_ind"):
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










with batting_team_tab:

    with open("batters.json", "r") as file:
        batters = json.load(file)

    st.title("2025 College Baseball Batting Stats")

    team_name = st.selectbox(
        "Team",
        list(batters.keys()),
        index=list(batters.keys()).index("CLEM"),
        key="batting_team_team"
    )

    with open("batting_metrics_map.json", "r") as file:
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

        st.plotly_chart(fig)

with pitching_team_tab:

    with open("pitchers.json", "r") as file:
        pitchers = json.load(file)

    st.title("2025 College Baseball Pitching Stats")

    team_name = st.selectbox(
        "Team",
        list(pitchers.keys()),
        index=list(pitchers.keys()).index("CLEM"),
        key="pitching_team_team"
    )

    with open("pitching_metrics_map.json", "r") as file:
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

        st.plotly_chart(fig)
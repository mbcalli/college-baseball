import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from helper import *
import json

with open("players.json", "r") as file:
    players = json.load(file)

st.title("2025 College Baseball Batting Stats")

team_name = st.selectbox(
    "Team",
    list(players.keys()),
    index=list(players.keys()).index("CLEM")
)

player_name = st.selectbox(
    "Batter",
    players[team_name]
)

if st.button("Show"):
    connection = sqlite3.connect("baseball.db")
    raw_batting = pd.read_sql(f"SELECT * FROM raw_batting WHERE name = '{player_name}'", connection)
    processed_batting = pd.read_sql(f"SELECT * FROM processed_batting WHERE name = '{player_name}'", connection)
    connection.close()

    fig = get_player_batting_figure(player_name, processed_batting, raw_batting)

    st.plotly_chart(fig)
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

def get_batter_df(player_name: str, silver_adv_batting: pd.DataFrame, bronze_adv_batting: pd.DataFrame) -> pd.DataFrame:

    player_processed = silver_adv_batting[silver_adv_batting["name"] == player_name]
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

    player_raw = bronze_adv_batting[bronze_adv_batting["name"] == player_name]
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

def get_player_batting_figure(player_name: str, silver_adv_batting: pd.DataFrame, bronze_adv_batting: pd.DataFrame):

    player_df = get_batter_df(player_name, silver_adv_batting, bronze_adv_batting)

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
        margin=dict(l=0, r=0),
        yaxis=dict(
            showgrid=False
        ),
        yaxis2=dict(
            showgrid=False
        ),
        title=f"Batting - {player_name}"
    )

    fig.update_xaxes(
        row=1, col=1,
        tickmode="array",
        tickvals=[10, 50, 90],
        ticktext=["POOR", "AVERAGE", "GREAT"],
        side="top"
    )

    # Hide second subplot x-axis ticks/labels if desired
    fig.update_xaxes(
        row=1, col=2,
        showticklabels=False
    )

    return fig

def get_pitcher_df(player_name: str, silver_adv_pitching: pd.DataFrame, bronze_adv_pitching: pd.DataFrame) -> pd.DataFrame:

    player_processed = silver_adv_pitching[silver_adv_pitching["name"] == player_name]
    player_processed = player_processed.drop(columns=["id", "name", "team"]).T.reset_index()
    player_processed.columns = ["stat", "perc"]
    player_processed["stat"] = [
        "IP",
        "K/9",
        "BB/9",
        "K/BB",
        "HR/9",
        "K%",
        "BB%",
        "K-BB%",
        "AVG",
        "WHIP",
        "BABIP",
        "LOB%",
        "ERA",
        "FIP",
        "ERA-FIP"
    ]

    player_raw = bronze_adv_pitching[bronze_adv_pitching["name"] == player_name]
    player_raw = player_raw.drop(columns=["id", "name", "team", "age", "alt_name"]).T.reset_index()
    player_raw.columns = ["stat", "value"]
    player_raw["stat"] = [
        "IP",
        "K/9",
        "BB/9",
        "K/BB",
        "HR/9",
        "K%",
        "BB%",
        "K-BB%",
        "AVG",
        "WHIP",
        "BABIP",
        "LOB%",
        "ERA",
        "FIP",
        "ERA-FIP"
    ]

    player_df = pd.merge(left=player_processed, right=player_raw, on="stat")


    # player_df["color"] = player_df["perc"].apply(perc_to_color)
    player_df["color"] = player_df["perc"].apply(perc_to_pastel_color)
    player_df["value_str"] = player_df["value"].apply(value_to_string)
    player_df = player_df.iloc[::-1]

    return player_df

def get_player_pitching_figure(player_name: str, silver_adv_pitching: pd.DataFrame, bronze_adv_pitching: pd.DataFrame):

    player_df = get_pitcher_df(player_name, silver_adv_pitching, bronze_adv_pitching)

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
        yaxis=dict(
            showgrid=False
        ),
        yaxis2=dict(
            showgrid=False
        ),
        title=f"Pitching - {player_name}"
    )

    fig.update_xaxes(
        row=1, col=1,
        tickmode="array",
        tickvals=[10, 50, 90],
        ticktext=["POOR", "AVERAGE", "GREAT"],
        side="top"
    )

    # Hide second subplot x-axis ticks/labels if desired
    fig.update_xaxes(
        row=1, col=2,
        showticklabels=False
    )

    return fig

def get_team_stat_batting_df(team: str, stat: str, stat_fmt: str, min_pa: int = None) -> pd.DataFrame:

    connection = sqlite3.connect("baseball.db")
    raw_team = pd.read_sql(f"SELECT * FROM bronze_adv_batting where team = '{team}'", connection)
    processed_team = pd.read_sql(f"SELECT * FROM silver_adv_batting where team = '{team}'", connection)
    connection.close()

    if min_pa:
        raw_team = raw_team[raw_team["pa"] >= min_pa]

    team_stat_df = pd.merge(
        left=processed_team[["name", f"{stat.lower()}_percentile"]],
        right=raw_team[["name", stat.lower()]],
        on="name",
        how="inner"
    )

    team_stat_df = team_stat_df.sort_values(by=f"{stat.lower()}_percentile", ascending=True)

    team_stat_df.columns = ["name", "perc", "value"]

    team_stat_df["color"] = team_stat_df["perc"].apply(perc_to_pastel_color)
    team_stat_df["value_str"] = team_stat_df["value"].apply(value_to_string)

    return team_stat_df

def get_team_stat_batting_fig(team: str, stat: str, stat_fmt: str, min_pa: int = None):

    team_stat_batting_df = get_team_stat_batting_df(team, stat, stat_fmt, min_pa)
    
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
            x=[100] * len(team_stat_batting_df),
            y=team_stat_batting_df["name"],
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
            x=team_stat_batting_df["perc"],
            y=team_stat_batting_df["name"],
            orientation="h",
            marker_color=team_stat_batting_df["color"],
            text=team_stat_batting_df["perc"],
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
            x=[0] * len(team_stat_batting_df),
            y=team_stat_batting_df["name"],
            mode="text",
            text=team_stat_batting_df["value_str"],  # replace with your column
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
        yaxis=dict(
            showgrid=False
        ),
        yaxis2=dict(
            showgrid=False
        ),
        title=fr"Team: {team} | Stat: {stat_fmt}"
    )

    fig.update_xaxes(
        row=1, col=1,
        tickmode="array",
        tickvals=[10, 50, 90],
        ticktext=["POOR", "AVERAGE", "GREAT"],
        side="top"
    )

    # Hide second subplot x-axis ticks/labels if desired
    fig.update_xaxes(
        row=1, col=2,
        showticklabels=False
    )

    return fig

def get_team_stat_pitching_df(team: str, stat: str, stat_fmt: str, min_ip: int = None) -> pd.DataFrame:

    connection = sqlite3.connect("baseball.db")
    raw_team = pd.read_sql(f"SELECT * FROM bronze_adv_pitching where team = '{team}'", connection)
    processed_team = pd.read_sql(f"SELECT * FROM silver_adv_pitching where team = '{team}'", connection)
    connection.close()

    if min_ip:
        raw_team = raw_team[raw_team["ip"] >= min_ip]

    team_stat_df = pd.merge(
        left=processed_team[["name", f"{stat.lower()}_percentile"]],
        right=raw_team[["name", stat.lower()]],
        on="name",
        how="inner"
    )

    team_stat_df = team_stat_df.sort_values(by=f"{stat.lower()}_percentile", ascending=True)

    team_stat_df.columns = ["name", "perc", "value"]

    team_stat_df["color"] = team_stat_df["perc"].apply(perc_to_pastel_color)
    team_stat_df["value_str"] = team_stat_df["value"].apply(value_to_string)

    return team_stat_df

def get_team_stat_pitching_fig(team: str, stat: str, stat_fmt: str, min_ip: int = None):

    team_stat_pitching_df = get_team_stat_pitching_df(team, stat, stat_fmt, min_ip)
    
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
            x=[100] * len(team_stat_pitching_df),
            y=team_stat_pitching_df["name"],
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
            x=team_stat_pitching_df["perc"],
            y=team_stat_pitching_df["name"],
            orientation="h",
            marker_color=team_stat_pitching_df["color"],
            text=team_stat_pitching_df["perc"],
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
            x=[0] * len(team_stat_pitching_df),
            y=team_stat_pitching_df["name"],
            mode="text",
            text=team_stat_pitching_df["value_str"],  # replace with your column
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
        yaxis=dict(
            showgrid=False
        ),
        yaxis2=dict(
            showgrid=False
        ),
        title=fr"Team: {team} | Stat: {stat_fmt}"
    )

    fig.update_xaxes(
        row=1, col=1,
        tickmode="array",
        tickvals=[10, 50, 90],
        ticktext=["POOR", "AVERAGE", "GREAT"],
        side="top"
    )

    # Hide second subplot x-axis ticks/labels if desired
    fig.update_xaxes(
        row=1, col=2,
        showticklabels=False
    )

    return fig



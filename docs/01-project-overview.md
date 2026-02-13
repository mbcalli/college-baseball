# Project Overview

## Purpose

The College Baseball Statistics project is designed to provide a user-friendly interface for analyzing college baseball player performance using percentile-based metrics. Inspired by MLB's [Baseball Savant](https://baseballsavant.mlb.com/), this tool helps coaches, scouts, analysts, and fans evaluate players within the context of their peers.

## Motivation

Traditional baseball statistics (batting average, ERA, etc.) can be difficult to interpret in isolation. A .198 batting average might seem poor, but understanding that 77% of other players have higher batting averages provides crucial context. This project addresses that challenge by:

1. **Converting absolute statistics to percentiles**: Makes it easy to understand how a player ranks nationally
2. **Handling inverted metrics**: Some stats are better when lower (e.g., strikeout rate). The percentiles account for this automatically
3. **Providing context**: Minimum playing time filters help avoid inflated statistics from small sample sizes
4. **Enabling comparisons**: Side-by-side evaluation of team lineups and bullpens

## Key Concepts

### Percentiles

Percentiles represent how a player ranks relative to all other players:
- **99th percentile**: Better than 99% of players (excellent)
- **50th percentile**: Average
- **1st percentile**: Better than only 1% of players (poor)

### Inverted Metrics

Some statistics are better when lower (e.g., K% for batters, ERA for pitchers). The system automatically inverts these so higher percentiles always mean better performance.

### Playing Time Context

Raw statistics can be misleading with limited playing time. A player who is 3-for-3 has a 1.000 batting average, but this is less meaningful than a .350 average over 300 plate appearances. The tool provides minimum PA/IP filters to ensure meaningful comparisons.

## Use Cases

### Player Evaluation
- Scout potential recruits by comparing percentiles across key metrics
- Identify strengths and weaknesses in a player's game
- Track player development over time

### Team Analysis
- Build optimal lineups based on statistical profiles
- Evaluate bullpen depth and effectiveness
- Compare your team to national competition

### Strategic Decisions
- Identify matchup advantages
- Determine which stats correlate with team success
- Make data-driven roster decisions

## Data Coverage

The application includes:
- **Batting Statistics**: Standard (H, HR, RBI, etc.) and Advanced (wRC+, wOBA, ISO, etc.)
- **Pitching Statistics**: Standard (W, ERA, K, etc.) and Advanced (FIP, WHIP, K-BB%, etc.)
- **All NCAA Division I teams**
- **Complete player rosters**

## Limitations

- Data is static and requires manual updates from Fangraphs
- Fangraphs membership required to access raw data
- No real-time updates during games
- Historical data limited to provided CSV files

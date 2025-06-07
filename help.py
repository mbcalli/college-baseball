import streamlit as st

st.markdown(
    """
    # Help Page
    
    ## Percentiles
    The bar graphs show the _percentiles_ of key statistics for a given player. Percentiles are relative metrics and help understand how good you are with respect to other players. For example, interpreting a batting average of 0.198 is hard - but what if you knew 77% of other players have higher batting averages? That's where the percentile can help. Higher percentiles mean better.

    **Note:** There are some statistics which are better when lower, consider K% for a batter (strikeout rate). The percentiles take this into account. A 99th percentile in K% means you strike out _less than_ 99% of other players.
    
    **Note:** It's also important to consider how much playing time a player has experienced. When in the lineup and bullpen pages, you'll see a minimum plate appearances and minimum innings pitched, which hedge for inflated stats where a player might be 3 for 3 and have the highest batting average (1.000) when compared to players who've had 300 plate appearances.
    
    ## Motivation

    This project was inspired by MLB's [baseball savant](https://baseballsavant.mlb.com/) leaderboard, which shows how different players compare across key metrics. A tool like this can be of great value, especially in evaluating players, lineups, and bullpens, _within the context of other players, lineups, and bullpens_.

    ## Data source
    The data provided here are static pulls from [fangraph's college leaderboard](https://www.fangraphs.com/leaders/college). Access to the raw data requires a membership.
    """
)
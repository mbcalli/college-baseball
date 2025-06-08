import streamlit as st

pages = [
    st.Page("pages/batting_individual.py", title="Individual Batting"),
    st.Page("pages/pitching_individual.py", title="Individual Pitching"),
    st.Page("pages/batting_team.py", title="Team Lineup"),
    st.Page("pages/pitching_team.py", title="Team Bullpen"),
    st.Page("pages/help.py", title="Help")
]


pg = st.navigation(pages)
pg.run()
import streamlit as st

pages = [
    st.Page("batting_individual.py", title="Individual Batting"),
    st.Page("pitching_individual.py", title="Individual Pitching"),
    st.Page("batting_team.py", title="Team Lineup"),
    st.Page("pitching_team.py", title="Team Bullpen")
]


pg = st.navigation(pages)
pg.run()
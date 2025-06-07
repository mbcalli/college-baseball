import streamlit as st

pages = {
    "Player Level": [
        st.Page("batting_individual.py", title="Batting"),
        st.Page("pitching_individual.py", title="Pitching"),
    ],
    "Team Level": [
        st.Page("batting_team.py", title="Batting"),
        st.Page("pitching_team.py", title="Pitching"),
    ]
}

pg = st.navigation(pages)
pg.run()
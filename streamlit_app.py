import streamlit as st
import requests

CLASSIC_LEAGUE_ID = 1099729

st.title("🎩 Positive Vibes Chairman")

if st.button("Test FPL Connection"):

    url = f"https://fantasy.premierleague.com/api/leagues-classic/{CLASSIC_LEAGUE_ID}/standings/"

    response = requests.get(url)

    st.write("Status Code:", response.status_code)

    if response.status_code == 200:
        st.success("Connected to FPL!")
        st.json(response.json())
    else:
        st.error("Could not connect.")

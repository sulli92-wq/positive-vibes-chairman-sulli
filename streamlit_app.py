import streamlit as st
import requests

CLASSIC_LEAGUE_ID = 1099729

st.title("🎩 Positive Vibes Chairman")

try:

    url = f"https://fantasy.premierleague.com/api/leagues-classic/{CLASSIC_LEAGUE_ID}/standings/"

    response = requests.get(url)
    data = response.json()

    st.success("Connected to FPL")

    standings = data["standings"]["results"]

    st.write(f"Found {len(standings)} managers")

    st.write("First manager record:")

    st.json(standings[0])

except Exception as e:
    st.error(str(e))

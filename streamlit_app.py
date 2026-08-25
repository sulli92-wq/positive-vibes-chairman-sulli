import streamlit as st
import requests

CLASSIC_LEAGUE_ID = 1099729

st.title("🎩 Positive Vibes Chairman")

url = f"https://fantasy.premierleague.com/api/leagues-classic/{CLASSIC_LEAGUE_ID}/standings/"
data = requests.get(url).json()

st.write("Standings object:")
st.json(data["standings"])

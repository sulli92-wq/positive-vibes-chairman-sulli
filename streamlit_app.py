import streamlit as st
import requests

CLASSIC_LEAGUE_ID = 1099729

st.title("🎩 Positive Vibes Chairman")

url = f"https://fantasy.premierleague.com/api/leagues-classic/{CLASSIC_LEAGUE_ID}/standings/"

response = requests.get(url)

st.write("Status Code:", response.status_code)

data = response.json()

st.write("Top Level Keys:")
st.write(list(data.keys()))

st.write("Full Response:")
st.json(data)

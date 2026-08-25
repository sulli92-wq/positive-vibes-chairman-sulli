import streamlit as st
import requests

CLASSIC_LEAGUE_ID = 1099729

st.title("🎩 Positive Vibes Chairman")

data = requests.get(
    f"https://fantasy.premierleague.com/api/leagues-classic/{CLASSIC_LEAGUE_ID}/standings/"
).json()

standings = data["standings"]["results"]

winner = max(standings, key=lambda x: x["event_total"])
loser = min(standings, key=lambda x: x["event_total"])

report = f"""
🎩 POSITIVE VIBES BOARD STATEMENT

🏆 CHAIRMAN'S MEDAL

{winner["player_name"]}
{winner["event_total"]} points

🥄 WOODEN SPOON

{loser["player_name"]}
{loser["event_total"]} points

Fine Issued: £10

Current Leader:
{winner["player_name"]}

Chairman's Verdict

The board thanks all managers for their continued contributions to the fine fund.
"""

st.text_area(
    "Chairman's Report",
    report,
    height=400
)

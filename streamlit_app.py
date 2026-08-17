import streamlit as st
import requests
import pandas as pd

CLASSIC_LEAGUE_ID = 1099729

st.set_page_config(
    page_title="Positive Vibes Chairman",
    page_icon="🎩"
)

def get_league_data():
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{CLASSIC_LEAGUE_ID}/standings/"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None


def generate_report():

    data = get_league_data()

    if not data:
        return "Unable to retrieve league data."

    standings = data["standings"]["results"]

    winner = max(standings, key=lambda x: x["event_total"])
    loser = min(standings, key=lambda x: x["event_total"])

    report = f"""
🎩 POSITIVE VIBES BOARD STATEMENT

🏆 CHAIRMAN'S MEDAL

{winner['player_name']}
{winner['event_total']} points

The board congratulates this week's top performer.

🥄 WOODEN SPOON

{loser['player_name']}
{loser['event_total']} points

Fine issued: £10

Chairman's Verdict

The board notes another week of highly questionable decision making and thanks all managers for their continued contribution to the fine pot.
"""

    return report


st.title("🎩 Positive Vibes Chairman")

st.write("League ID: 1099729")

if st.button("Generate Chairman Report"):

    report = generate_report()

    st.text_area(
        "Copy into iMessage",
        report,
        height=500
    )

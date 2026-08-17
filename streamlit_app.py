import streamlit as st

st.set_page_config(
    page_title="Positive Vibes Chairman",
    page_icon="🎩"
)

st.title("🎩 Positive Vibes Chairman")

st.write("""
Welcome to the Positive Vibes Chairman Portal.

League Rules:

🥄 Lowest Gameweek Score = £10 Fine

🎰 Chip Used But No GW Win = £5 Fine

📊 Lose To AVERAGE In H2H = £10 Fine
""")

if st.button("Generate Chairman Report"):

    report = """
🎩 POSITIVE VIBES BOARD STATEMENT

GAMEWEEK 1

🏆 Chairman's Medal

Winner TBC

🥄 Wooden Spoon

Loser TBC

Fine Issued: £10

🎰 Chip Department

No offences recorded.

📊 Average FC Tribunal

No offences recorded.

The board thanks managers for their continued participation.
"""

    st.text_area(
        "Chairman's Report",
        report,
        height=400
    )

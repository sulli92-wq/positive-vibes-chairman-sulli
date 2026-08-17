import streamlit as st

st.set_page_config(
    page_title="Positive Vibes Chairman",
    page_icon="🎩"
)

st.title("🎩 Positive Vibes Chairman")

st.success("System operational")

st.write("""
League IDs configured:

✅ Classic League: 1099729

✅ H2H League: 1128355

Fine Rules:

🥄 Lowest Scorer = £10

🎰 Chip Used & No GW Win = £5

📊 Lose To AVERAGE = £10
""")

if st.button("Generate Report"):

    st.info("""
No Gameweek data available yet.

The Positive Vibes Chairman will become active once
Gameweek 1 has been completed.
""")
``

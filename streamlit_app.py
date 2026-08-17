def generate_report():

    data = get_league_data()

    if not data:
        return "Unable to retrieve league data."

    standings = data["standings"]["results"]

    if len(standings) == 0:
        return "No standings data returned."

    winner = standings[0]
    loser = standings[-1]

    winner_name = f"{winner['player_first_name']} {winner['player_last_name']}"
    loser_name = f"{loser['player_first_name']} {loser['player_last_name']}"

    report = f"""
🎩 POSITIVE VIBES BOARD STATEMENT

🏆 CHAIRMAN'S MEDAL

{winner_name}

Overall Rank: {winner['rank']}

🥄 WOODEN SPOON

{loser_name}

Overall Rank: {loser['rank']}

Fine Issued: £10

Chairman's Verdict

The board notes another week of highly questionable decision making and thanks all managers for their continued contribution to the fine pot.
"""

    return report

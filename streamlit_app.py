import streamlit as st
import requests
import pandas as pd

# ---------------------------------------------------------
# POSITIVE VIBES SETTINGS
# ---------------------------------------------------------

CLASSIC_LEAGUE_ID = 1099729
H2H_LEAGUE_ID = 1128355

WOODEN_SPOON_FINE = 10
FAILED_CHIP_FINE = 5
AVERAGE_FINE = 10

BASE_URL = "https://fantasy.premierleague.com/api"

CHIP_NAMES = {
    "wildcard": "Wildcard",
    "freehit": "Free Hit",
    "bboost": "Bench Boost",
    "3xc": "Triple Captain",
}


# ---------------------------------------------------------
# STREAMLIT PAGE
# ---------------------------------------------------------

st.set_page_config(
    page_title="Positive Vibes Chairman",
    page_icon="🎩",
    layout="centered",
)

st.title("🎩 Positive Vibes Chairman")
st.caption("Weekly fines and Chairman's Report generator")


# ---------------------------------------------------------
# API FUNCTIONS
# ---------------------------------------------------------

def get_json(url, params=None):
    headers = {
        "User-Agent": "Positive-Vibes-FPL-Chairman/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def get_bootstrap_data():
    return get_json(f"{BASE_URL}/bootstrap-static/")


@st.cache_data(ttl=300)
def get_classic_league():
    return get_json(
        f"{BASE_URL}/leagues-classic/"
        f"{CLASSIC_LEAGUE_ID}/standings/"
    )


@st.cache_data(ttl=300)
def get_manager_picks(entry_id, gameweek):
    return get_json(
        f"{BASE_URL}/entry/"
        f"{entry_id}/event/{gameweek}/picks/"
    )


@st.cache_data(ttl=300)
def get_h2h_matches(gameweek):
    """
    FPL's H2H URL has changed format in some seasons.
    This function tries the known public variants.
    """

    possible_requests = [
        (
            f"{BASE_URL}/leagues-h2h-matches/"
            f"league/{H2H_LEAGUE_ID}/",
            {"event": gameweek},
        ),
        (
            f"{BASE_URL}/leagues-h2h-matches/"
            f"league/{H2H_LEAGUE_ID}/",
            {"event": gameweek, "page": 1},
        ),
        (
            f"{BASE_URL}/leagues-h2h/"
            f"{H2H_LEAGUE_ID}/matches/",
            {"event": gameweek},
        ),
    ]

    last_error = None

    for url, params in possible_requests:
        try:
            data = get_json(url, params=params)

            if isinstance(data, dict):
                results = data.get("results", [])

                if results:
                    return results

                matches = data.get("matches", [])

                if matches:
                    return matches

            if isinstance(data, list) and data:
                return data

        except Exception as error:
            last_error = error

    if last_error:
        raise last_error

    return []


# ---------------------------------------------------------
# GAMEWEEK FUNCTIONS
# ---------------------------------------------------------

def get_latest_completed_gameweek():
    bootstrap = get_bootstrap_data()
    events = bootstrap.get("events", [])

    fully_checked = [
        event
        for event in events
        if event.get("finished")
        and event.get("data_checked")
    ]

    if fully_checked:
        return max(
            fully_checked,
            key=lambda event: event["id"],
        )["id"]

    finished = [
        event
        for event in events
        if event.get("finished")
    ]

    if finished:
        return max(
            finished,
            key=lambda event: event["id"],
        )["id"]

    return None


def get_gameweek_options():
    bootstrap = get_bootstrap_data()
    events = bootstrap.get("events", [])

    completed_ids = [
        event["id"]
        for event in events
        if event.get("finished")
    ]

    return sorted(completed_ids, reverse=True)


# ---------------------------------------------------------
# LEAGUE DATA
# ------------------------------------------------
st.success("Version 2 interface reached")
try:
    bootstrap = get_bootstrap_data()
    events = bootstrap.get("events", [])

    st.write("FPL gameweek status:")

    event_rows = []

    for event in events:
        if event.get("id") == 1:
            event_rows.append({
                "Gameweek": event.get("id"),
                "Finished": event.get("finished"),
                "Data checked": event.get("data_checked"),
                "Current": event.get("is_current"),
                "Previous": event.get("is_previous"),
                "Average score": event.get("average_entry_score"),
            })

    st.dataframe(
        pd.DataFrame(event_rows),
        use_container_width=True,
        hide_index=True,
    )

    available_gameweeks = [
        event["id"]
        for event in events
        if event.get("finished")
        or event.get("data_checked")
        or event.get("is_previous")
    ]

    available_gameweeks = sorted(
        set(available_gameweeks),
        reverse=True,
    )

    if not available_gameweeks:
        st.warning(
            "FPL has not marked any gameweek as finished yet. "
            "Gameweek 1 can still be tested manually below."
        )
        available_gameweeks = [1]

    selected_gameweek = st.selectbox(
        "Choose gameweek",
        options=available_gameweeks,
        format_func=lambda gw: f"Gameweek {gw}",
    )

    if st.button(
        "Generate Chairman's Report",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Reviewing the gameweek..."):
            result = generate_chairman_data(selected_gameweek)

        st.success(
            f"Gameweek {selected_gameweek} report generated."
        )

        st.subheader("Copy into iMessage")

        st.text_area(
            "Chairman's Report",
            value=result["report"],
            height=700,
        )

        st.subheader("Gameweek fines")

        if result["fine_rows"]:
            fine_table = pd.DataFrame(result["fine_rows"])

            fine_table["Reasons"] = (
                fine_table["Reasons"]
                .apply(lambda reasons: "; ".join(reasons))
            )

            fine_table["Fine"] = (
                fine_table["Fine"]
                .apply(lambda value: f"£{value}")
            )

            st.dataframe(
                fine_table,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(
                "No fines were calculated for this gameweek."
            )

        with st.expander("Full gameweek standings"):
            standings_table = pd.DataFrame(
                [
                    {
                        "Manager": row["manager"],
                        "Team": row["team"],
                        "GW Points": row["gw_points"],
                        "Chip": row["chip_name"] or "None",
                        "Overall Points": row["overall_points"],
                        "League Rank": row["rank"],
                    }
                    for row in sorted(
                        result["manager_rows"],
                        key=lambda item: (
                            -item["gw_points"],
                            item["manager"],
                        ),
                    )
                ]
            )

            st.dataframe(
                standings_table,
                use_container_width=True,
                hide_index=True,
            )

        if result["h2h_error"]:
            st.warning(
                "The Classic League and chip checks worked, "
                "but the H2H check failed. Technical detail: "
                f"{result['h2h_error']}"
            )

        elif result["h2h_match_count"] == 0:
            st.warning(
                "No H2H fixtures were returned, so the "
                "AVERAGE fine was not applied."
            )

except Exception as error:
    st.error("The Version 2 interface encountered an error.")
    st.exception(error)

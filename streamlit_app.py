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

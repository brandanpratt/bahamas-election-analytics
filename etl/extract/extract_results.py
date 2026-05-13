import requests
import pandas as pd

URL = (
    "https://www.bahamas2026.com/"
    "api/live/candidates"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7)"
    )
}

PARTY_MAPPING = {
    "IND": "Independent"
}

CONSTITUENCY_MAPPING = {

    "Bains Town and Grants Town":
        "Bains Town and Grants Town",

    "Bamboo Town":
        "Bamboo Town",

    "Bimini and The Berry Islands":
        "Bimini and the Berry Islands",

    "Carmichael":
        "Carmichael",

    "Cat Island, Rum Cay & San Salvador":
        "Cat Island, Rum Cay and San Salvador",

    "Central & South Abaco":
        "Central and South Abaco",

    "Central and South Eleuthera":
        "Central and South Eleuthera",

    "Central Grand Bahama":
        "Central Grand Bahama",

    "Central, Mangrove Cay, and South Andros":
        "Central and South Andros",

    "Centreville":
        "Centreville",

    "East Grand Bahama":
        "East Grand Bahama",

    "Elizabeth":
        "Elizabeth",

    "Englerston":
        "Englerston",

    "Exumas & Ragged Island":
        "Exuma and Ragged Island",

    "Fort Charlotte":
        "Fort Charlotte",

    "Fox Hill":
        "Fox Hill",

    "Freetown":
        "Freetown",

    "Garden Hills":
        "Garden Hills",

    "Golden Gates":
        "Golden Gates",

    "Golden Isles":
        "Golden Isles",

    "Killarney":
        "Killarney",

    "Long Island":
        "Long Island",

    "Marathon":
        "Marathon",

    "Marco City":
        "Marco City",

    "Mayaguana, Inagua, Crooked Island, Acklins and Long Cay":
        "MICAL",

    "Mount Moriah":
        "Mount Moriah",

    "Nassau Village":
        "Nassau Village",

    "North Abaco":
        "North Abaco",

    "North Andros":
        "North Andros",

    "North Eleuthera":
        "North Eleuthera",

    "Pineridge":
        "Pineridge",

    "Pinewood":
        "Pinewood",

    "Saint Anne's":
        "St. Anne's",

    "Seabreeze":
        "Seabreeze",

    "South Beach":
        "South Beach",

    "Southern Shores":
        "Southern Shores",

    "St. Barnabas":
        "St. Barnabas",

    "St. James":
        "St. James",

    "Tall Pines":
        "Tall Pines",

    "West Grand Bahama":
        "West Grand Bahama",

    "Yamacraw":
        "Yamacraw"
}

def normalize_party(party):

    return PARTY_MAPPING.get(
        party,
        party
    )

def normalize_constituency(name):

    return CONSTITUENCY_MAPPING.get(
        name,
        name
    )

def extract_results():

    try:

        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print(f"Request failed: {e}")

        return pd.DataFrame()

    data = response.json()

    rows = []

    for race in data.get(
        "races",
        []
    ):

        constituency = normalize_constituency(
            race.get("constituency")
        )

        island = race.get("island")

        total_votes = race.get(
            "total_votes"
        )

        leader_party = race.get(
            "leader_party"
        )

        for candidate in race.get(
            "candidates",
            []
        ):

            rows.append({

                "constituency":
                    constituency,

                "island":
                    island,

                "candidate_name":
                    candidate.get("name"),

                "party":
                    normalize_party(
                        candidate.get("party")
                    ),

                "votes":
                    candidate.get("votes"),

                "vote_percentage":
                    candidate.get("pct"),

                "is_incumbent":
                    candidate.get(
                        "is_incumbent"
                    ),

                "leading":
                    (
                        candidate.get("party")
                        == leader_party
                    ),

                "total_votes":
                    total_votes,

                "source":
                    "Bahamas2026"
            })

    df = pd.DataFrame(rows)

    return df
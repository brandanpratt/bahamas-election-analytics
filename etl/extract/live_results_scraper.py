import requests
import pandas as pd
import json

from datetime import datetime

URL = "https://www.bahamas2026.com/api/live/results"

MOCK_MODE = False

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7)"
    )
}

CONSTITUENCY_MAPPING = {
    "Bains Town and Grants Town":
        "Bain Town and Grants Town",

    "Sea Breeze":
        "Seabreeze",

    "Saint Barnabas":
        "St. Barnabas",

    "Saint Anne's":
        "St. Anne's",

    "Cat Island, Rum Cay and San Salvador":
        "Rum Cay and San Salvador",

    "The Exumas and Ragged Island":
        "Exuma and Ragged Island",

    "North Andros and Berry Islands":
        "North Andros"
}

def normalize_constituency(name):

    return CONSTITUENCY_MAPPING.get(
        name,
        name
    )

def scrape_live_results():

    try:

        if MOCK_MODE:

            with open(
                "data/mock_live_results.json"
            ) as f:

                data = json.load(f)

            print(
                "Using mock election data."
            )

        else:

            response = requests.get(
                URL,
                headers=HEADERS,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            print(
                "Using live election API."
            )

    except Exception as e:

        print(f"Request failed: {e}")

        return pd.DataFrame()

    timestamp = datetime.now()

    results = []

    statuses = data.get(
        "statuses",
        []
    )

    for status in statuses:

        constituency = normalize_constituency(
            status.get(
                "constituency_name"
            )
        )

        results.append({
            "constituency":
                constituency,

            "status":
                status.get("status"),

            "called_party":
                status.get("called_party"),

            "reporting_percentage":
                status.get("pct_reported"),

            "turnout_percentage":
                status.get("turnout_pct"),

            "source":
                "Bahamas2026",

            "ingestion_timestamp":
                timestamp
        })

    df = pd.DataFrame(results)

    return df

if __name__ == "__main__":

    df = scrape_live_results()

    print(df.head())
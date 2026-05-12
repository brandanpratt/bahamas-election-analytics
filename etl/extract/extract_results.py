import requests
import pandas as pd

URL = "https://www.bahamas2026.com/api/live/results"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7)"
    )
}

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

    results = []

    statuses = data.get(
        "statuses",
        []
    )

    for status in statuses:

        results.append({
            "constituency":
                status.get("constituency_name"),

            "candidate_name":
                status.get("candidate_name"),

            "party":
                status.get("called_party"),

            "votes":
                status.get("votes"),

            "reporting_percentage":
                status.get("pct_reported"),

            "leading":
                True,

            "source":
                "Bahamas2026"
        })

    df = pd.DataFrame(results)

    return df
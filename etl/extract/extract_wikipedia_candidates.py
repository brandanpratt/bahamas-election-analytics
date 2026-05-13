import pandas as pd
import requests
from io import StringIO

URL = "https://en.wikipedia.org/wiki/2026_Bahamian_general_election"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

def clean_constituency(name):

    replacements = {
        "Bains Town and Grants Town": "Bains Town and Grants Town",
        "Sea Breeze": "Seabreeze",
        "Saint Barnabas": "St. Barnabas",
        "Saint Anne's": "St. Anne's",
        "Cat Island, Rum Cay & San Salvador": "Rum Cay and San Salvador",
        "The Exumas and Ragged Island": "Exuma and Ragged Island",
        "Bimini and Berry Islands": "Bimini and the Berry Islands"
    }

    return replacements.get(name.strip(), name.strip())

def extract_candidates():

    response = requests.get(URL, headers=HEADERS)

    html = response.text

    tables = pd.read_html(StringIO(html))

    target_table = None

    for table in tables:

        columns = [str(col) for col in table.columns]

        if "Constituency" in columns:

            target_table = table
            break

    if target_table is None:
        raise Exception("Candidate table not found.")

    candidates = []

    for _, row in target_table.iterrows():

        constituency = clean_constituency(
            str(row["Constituency"])
        )

        party_mapping = {
            "PLP": row["PLP"],
            "FNM": row["FNM"],
            "COI": row["COI"]
        }

        for party, candidate in party_mapping.items():

            if pd.notna(candidate):

                candidates.append({
                    "constituency": constituency,
                    "candidate_name": str(candidate).strip(),
                    "party": party,
                    "source": "Wikipedia"
                })

        independents = row["Independent"]

        if pd.notna(independents):

            independent_list = str(independents).split(",")

            for candidate in independent_list:

                candidates.append({
                    "constituency": constituency,
                    "candidate_name": candidate.strip(),
                    "party": "Independent",
                    "source": "Wikipedia"
                })

    df = pd.DataFrame(candidates)

    return df
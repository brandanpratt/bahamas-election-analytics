import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.fnmbahamas.org/candidates/"

VALID_CONSTITUENCIES = [
    "Bains Town and Grants Town",
    "Bamboo Town",
    "Carmichael",
    "Centreville",
    "Elizabeth",
    "Englerston",
    "Fort Charlotte",
    "Fox Hill",
    "Free Town",
    "Garden Hills",
    "Golden Gates",
    "Golden Isles",
    "Killarney",
    "Marathon",
    "Mount Moriah",
    "Nassau Village",
    "Pinewood",
    "St. Barnabas",
    "St. James",
    "Seabreeze",
    "South Beach",
    "Southern Shores",
    "Tall Pines",
    "Yamacraw",
    "Central Grand Bahama",
    "East Grand Bahama",
    "Marco City",
    "Pineridge",
    "West Grand Bahama",
    "Central and South Abaco",
    "North Abaco",
    "Mangrove Cay and South Andros",
    "North Andros",
    "Bimini and the Berry Islands",
    "Rum Cay and San Salvador",
    "Central and South Eleuthera",
    "North Eleuthera",
    "Long Island",
    "Acklins and Long Cay"
]

def clean_text(text):

    return (
        text.replace("Sea Breeze", "Seabreeze")
        .replace("Centrevile", "Centreville")
        .replace("St. Anne’s", "St. Anne's")
        .strip()
    )

def extract_fnm_candidates():

    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")

    lines = [
        clean_text(line.strip())
        for line in soup.get_text("\n").split("\n")
        if line.strip()
    ]

    candidates = []

    for i in range(len(lines) - 1):

        current_line = lines[i]
        next_line = lines[i + 1]

        if current_line in VALID_CONSTITUENCIES:

            if next_line not in VALID_CONSTITUENCIES:

                candidates.append({
                    "constituency": current_line,
                    "candidate_name": next_line,
                    "party": "FNM"
                })

    df = pd.DataFrame(candidates)

    df = df.drop_duplicates()

    return df

if __name__ == "__main__":

    df = extract_fnm_candidates()

    print(df)

    df.to_csv("data/fnm_candidates_clean.csv", index=False)
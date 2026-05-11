import pdfplumber
import pandas as pd
import re

PDF_PATH = "2026-0001.pdf"

def extract_constituencies():

    constituencies = []

    with pdfplumber.open(PDF_PATH) as pdf:

        full_text = ""

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                full_text += text + "\n"

    pattern = r"([A-Z\s\.\-']+)\sCONSTITUENCY"

    matches = re.findall(pattern, full_text)

    cleaned = []

    for match in matches:

        constituency = match.strip().title()

        if constituency not in cleaned:
            cleaned.append(constituency)

    for constituency in cleaned:

        constituencies.append({
            "constituency": constituency
        })

    df = pd.DataFrame(constituencies)

    return df

if __name__ == "__main__":

    df = extract_constituencies()

    df.to_csv("data/constituencies_extracted.csv", index=False)
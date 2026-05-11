from etl.extract.extract_wikipedia_candidates import extract_candidates
from etl.load.load_candidates import load_candidates

def run_pipeline():

    df = extract_candidates()

    print(df.head())

    load_candidates(df)

if __name__ == "__main__":
    run_pipeline()
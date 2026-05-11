from etl.extract.extract_results import extract_results
from etl.load.load_results import load_results

def run_pipeline():

    df = extract_results()

    print(df.head())

    load_results(df)

if __name__ == "__main__":
    run_pipeline()
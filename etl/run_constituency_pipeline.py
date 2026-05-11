from etl.extract.extract_constituencies import extract_constituencies
from etl.load.load_constituencies import load_constituencies

def run_pipeline():

    df = extract_constituencies()

    load_constituencies(df)

if __name__ == "__main__":
    run_pipeline()
from sqlalchemy import text

from etl.extract.extract_results import (
    extract_results
)

from etl.load.load_results import (
    load_results
)

from etl.load.snowflake_connection import (
    get_snowflake_engine
)

def run_pipeline():

    df = extract_results()

    if df.empty:

        print(
            "No live election data returned."
        )

        return

    print(df.head())

    engine = get_snowflake_engine()

    with engine.begin() as conn:

        conn.execute(
            text("""
                TRUNCATE TABLE
                ELECTION_DB.RAW.RESULTS
            """)
        )

    print(
        "RAW.RESULTS truncated successfully."
    )

    load_results(df)

if __name__ == "__main__":

    run_pipeline()
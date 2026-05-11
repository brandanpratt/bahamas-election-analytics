from etl.load.snowflake_connection import get_snowflake_engine

def load_candidates(df):

    engine = get_snowflake_engine()

    df.to_sql(
        "CANDIDATES",
        con=engine,
        schema="RAW",
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Candidates loaded successfully.")
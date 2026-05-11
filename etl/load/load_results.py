from etl.load.snowflake_connection import get_snowflake_engine

def load_results(df):

    engine = get_snowflake_engine()

    df.to_sql(
        "RESULTS",
        con=engine,
        schema="RAW",
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Results loaded successfully.")
from etl.load.snowflake_connection import get_snowflake_engine

def load_constituencies(df):

    engine = get_snowflake_engine()

    df.to_sql(
        "CONSTITUENCIES",
        con=engine,
        schema="RAW",
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Constituencies loaded successfully.")
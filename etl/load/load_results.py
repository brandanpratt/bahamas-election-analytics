from etl.load.snowflake_connection import get_snowflake_engine

TEST_MODE = False

def load_results(df):

    table_name = (
        "RESULTS_TEST"
        if TEST_MODE
        else "RESULTS"
    )

    engine = get_snowflake_engine()

    df.to_sql(
        table_name,
        con=engine,
        schema="RAW",
        if_exists="append",
        index=False,
        method="multi"
    )

    print(f"Results loaded into RAW.{table_name}")
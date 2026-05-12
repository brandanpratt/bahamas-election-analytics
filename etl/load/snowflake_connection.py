from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import streamlit as st
import os

load_dotenv()

SNOWFLAKE_USER = st.secrets.get(
    "SNOWFLAKE_USER",
    os.getenv("SNOWFLAKE_USER")
)

SNOWFLAKE_PASSWORD = quote_plus(
    st.secrets.get(
        "SNOWFLAKE_PASSWORD",
        os.getenv("SNOWFLAKE_PASSWORD")
    )
)

SNOWFLAKE_ACCOUNT = st.secrets.get(
    "SNOWFLAKE_ACCOUNT",
    os.getenv("SNOWFLAKE_ACCOUNT")
)

SNOWFLAKE_WAREHOUSE = st.secrets.get(
    "SNOWFLAKE_WAREHOUSE",
    os.getenv("SNOWFLAKE_WAREHOUSE")
)

SNOWFLAKE_DATABASE = st.secrets.get(
    "SNOWFLAKE_DATABASE",
    os.getenv("SNOWFLAKE_DATABASE")
)

SNOWFLAKE_SCHEMA = st.secrets.get(
    "SNOWFLAKE_SCHEMA",
    os.getenv("SNOWFLAKE_SCHEMA")
)

SNOWFLAKE_ROLE = st.secrets.get(
    "SNOWFLAKE_ROLE",
    os.getenv("SNOWFLAKE_ROLE")
)

def get_snowflake_engine():
    connection_url = (
        f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}"
        f"@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"
        f"?warehouse={SNOWFLAKE_WAREHOUSE}&role={SNOWFLAKE_ROLE}"
    )

    engine = create_engine(connection_url)

    return engine
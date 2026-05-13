import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from streamlit_autorefresh import st_autorefresh
import os

st.set_page_config(
    page_title="Bahamas Election Analytics Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = quote_plus(os.getenv("SNOWFLAKE_PASSWORD"))
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

connection_url = (
    f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}"
    f"@{SNOWFLAKE_ACCOUNT}/{SNOWFLAKE_DATABASE}"
    f"?warehouse={SNOWFLAKE_WAREHOUSE}&role={SNOWFLAKE_ROLE}"
)

@st.cache_resource
def get_engine():
    return create_engine(connection_url)

engine = get_engine()

st.title("Bahamas Election Analytics Platform 2026")

st.caption(
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

st.sidebar.success("Live Data Feed Connected")

st_autorefresh(interval=30000, key="live_results")

@st.cache_data(ttl=30)
def load_candidates():
    query = """
    SELECT
        candidate_name,
        party,
        constituency
    FROM RAW.CANDIDATES
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=30)
def load_seat_data():
    query = """
    SELECT
        party,
        seats_leading
    FROM MARTS.SEAT_COUNTS
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=30)
def load_vote_data():
    query = """
    SELECT
        party,
        total_votes
    FROM MARTS.PARTY_VOTE_SHARE
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=30)
def load_leaders_data():
    leaders_query ="""
    SELECT
        constituency,
        candidate_name,
        party,
        votes,
        vote_percentage,
        island
    FROM MARTS.CONSTITUENCY_LEADERS
    """

    return pd.read_sql(leaders_query, engine)

@st.cache_data(ttl=30)
def load_map_data():

    leaders_query = """
    SELECT
        constituency,
        candidate_name,
        party,
        votes,
        vote_percentage,
        island
    FROM MARTS.CONSTITUENCY_LEADERS
    """
    return pd.read_sql(query, engine)

@st.cache_data
def load_geojson():
    with open("data/bahamas_islands.geojson") as f:
        return json.load(f)

try:
    df = load_candidates()
    seat_df = load_seat_data()
    vote_df = load_vote_data()
    leaders_df = load_leaders_data()
    map_df = load_map_data()
    geojson_data = load_geojson()

except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

party_filter = st.sidebar.selectbox(
    "Select Party",
    ["All"] + sorted(df["party"].unique().tolist())
)

if party_filter != "All":

    df = df[df["party"] == party_filter]

    if not seat_df.empty:
        seat_df = seat_df[
            seat_df["party"] == party_filter
        ]

    if not vote_df.empty:
        vote_df = vote_df[
            vote_df["party"] == party_filter
        ]

    if not leaders_df.empty:
        leaders_df = leaders_df[
            leaders_df["party"] == party_filter
        ]

    if not map_df.empty:
        map_df = map_df[
            map_df["party"] == party_filter
        ]

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Live Results",
    "Election Map",
    "Candidates"
])

with tab1:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Candidates",
        len(df)
    )

    col2.metric(
        "Total Constituencies",
        df["constituency"].nunique()
    )

    party_count = (
    df[
        df["party"] != "Independent"
    ]["party"]
    .nunique()
    )

    col3.metric(
        "Political Parties",
        party_count
    )

    chart_df = df.copy()

    chart_df["party_display"] = chart_df.apply(
        lambda row:
            row["candidate_name"]
            if row["party"] == "Independent"
            else row["party"],
        axis=1
    )

    party_counts = (
        chart_df["party_display"]
        .value_counts()
    )
    st.subheader("Candidates by Party or Independent Status")
    st.bar_chart(party_counts)

    majority_needed = 21

    if seat_df.empty:

        st.warning("No seat count data available yet.")

    else:

        leading_party = (
            seat_df.sort_values(
                by="seats_leading",
                ascending=False
            ).iloc[0]
        )

        st.success(
            f"{leading_party['party']} leading with "
            f"{leading_party['seats_leading']} seats "
            f"({majority_needed} needed for majority)"
        )

with tab2:

    st.header("Seat Counts")

    if seat_df.empty:

        st.warning("No seat count data available.")

    else:

        st.dataframe(seat_df)

        st.bar_chart(
            seat_df.set_index("party")
        )

    st.header("Vote Share")

    if vote_df.empty:

        st.warning("No vote share data available.")

    else:

        st.dataframe(vote_df)

        st.bar_chart(
            vote_df.set_index("party")
        )

    st.header("Constituency Leaders")

    if leaders_df.empty:

        st.warning("No constituency leader data available.")

    else:

        st.dataframe(leaders_df)

with tab3:

    st.header("Election Map")

    if map_df.empty:

        st.warning("No map data available.")

    else:

        fig = px.choropleth_map(
            map_df,
            geojson=geojson_data,
            locations="constituency",
            featureidkey="properties.constituency",
            color="party",
            hover_name="constituency",
            hover_data=[
                "party",
                "votes",
                "vote_percentage"
            ],
            center={"lat": 24.25, "lon": -76.0},
            map_style="carto-positron",
            zoom=5,
            opacity=0.7
        )

        st.plotly_chart(fig, width="stretch")

with tab4:

    st.header("Candidates")

    st.dataframe(df)
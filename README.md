# Bahamas Election Analytics Platform 2026

A real-time election analytics platform built for the 2026 Bahamas General Election.

This project was designed to simulate a modern analytics engineering workflow around a live national event by combining real-time API ingestion, ETL pipelines, cloud data warehousing, and interactive election reporting into a single operational dashboard.

## Live Application

[Bahamas Election Analytics Platform 2026](https://bahamas-election-analytics.streamlit.app/?utm_source=chatgpt.com)

## Features

* Real-time constituency tracking
* Live seat count monitoring
* Interactive election map
* Real-time API ingestion pipelines
* Cloud-hosted analytics dashboard
* Party and constituency analytics
* Auto-refreshing live election updates
* Snowflake-powered analytics warehouse

## Tech Stack

### Data Engineering

* Python
* Pandas
* SQLAlchemy
* Snowflake
* REST APIs

### Analytics & Visualization

* Streamlit
* Plotly
* GeoJSON Mapping

### Infrastructure

* Streamlit Community Cloud
* GitHub

## Architecture

```text
Live Election APIs
        ↓
Python ETL Pipelines
        ↓
Snowflake Data Warehouse
        ↓
Analytics MARTS / SQL Views
        ↓
Streamlit Dashboard
        ↓
Interactive Election Visualizations
```

## Project Goals

The goal of this project was to explore how modern data engineering and analytics workflows could be applied to real-time election reporting in The Bahamas.

The platform was built to:

* ingest and process live election data
* model constituency-level analytics
* visualize election trends geographically
* simulate a production-style analytics environment under live operational conditions

## Key Learnings

This project provided hands-on experience with:

* real-time API ingestion
* ETL pipeline design
* cloud data warehousing
* analytics engineering workflows
* dashboard deployment
* operational monitoring
* geospatial election visualization

## Future Improvements

Planned future enhancements include:

* enhanced constituency boundary mapping
* candidate-level live vote ingestion
* turnout forecasting models
* automated orchestration workflows
* Power BI historical analytics layer
* advanced election intelligence reporting

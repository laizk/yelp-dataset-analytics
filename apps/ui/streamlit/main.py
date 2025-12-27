import os

import pandas as pd
import requests
import streamlit as st


ANALYTICS_API_URL = os.getenv("ANALYTICS_API_URL", "http://analytics-api:8001")

st.title("Main Dashboard")
st.write("Analytics API + quick chart demo.")

default_sql = "SELECT id, name FROM analytics_seed ORDER BY id"
sql = st.text_area("SQL", value=default_sql, height=120)

if st.button("Run query"):
    try:
        response = requests.post(
            f"{ANALYTICS_API_URL}/query/postgres",
            json={"sql": sql},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Query failed: {exc}")
        st.stop()

    rows = payload.get("rows", [])
    if not rows:
        st.info("No rows returned.")
        st.stop()

    df = pd.DataFrame(rows)
    st.dataframe(df)

    if "id" in df.columns and "name" in df.columns:
        chart_df = df.set_index("name")["id"]
        st.bar_chart(chart_df)

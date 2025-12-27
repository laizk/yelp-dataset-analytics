import os

import pandas as pd
import requests
import streamlit as st


SERVING_API_URL = os.getenv("SERVING_API_URL", "http://backend-serving-api:8010/api")
REVIEW_LIST_URL = f"{SERVING_API_URL.rstrip('/')}/reviews"

st.title("Reviews")
st.write("Recent reviews stored in MongoDB.")

limit = st.number_input("Limit", value=25, min_value=1, max_value=500, step=1)

if st.button("Load reviews"):
    try:
        response = requests.get(REVIEW_LIST_URL, params={"limit": limit}, timeout=10)
        response.raise_for_status()
        items = response.json().get("items", [])
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")
        st.stop()

    if not items:
        st.info("No reviews found.")
        st.stop()

    df = pd.DataFrame(items)
    st.dataframe(df)

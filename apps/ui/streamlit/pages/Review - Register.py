import os

import requests
import streamlit as st


SERVING_API_URL = os.getenv("SERVING_API_URL", "http://backend-serving-api:8010/api")
REVIEW_REGISTER_URL = f"{SERVING_API_URL.rstrip('/')}/reviews"

st.title("Register Review")
st.write("Create or update a review record in MongoDB via the serving API.")

with st.form("review_register_form"):
    col1, col2 = st.columns(2)
    with col1:
        review_id = st.text_input("Review ID", value="KU_O5udG6zpxOg-VcAEodg")
        user_id = st.text_input("User ID", value="mh_-eMZ6K5RLWhZyISBhwA")
        business_id = st.text_input("Business ID", value="XQfwVwDr-v0ZS3_CbbE5Xw")
        stars = st.number_input("Stars", value=3, min_value=0, max_value=5, step=1)
    with col2:
        useful = st.number_input("Useful", value=0, min_value=0, step=1, key="review_useful")
        funny = st.number_input("Funny", value=0, min_value=0, step=1, key="review_funny")
        cool = st.number_input("Cool", value=0, min_value=0, step=1, key="review_cool")
        date = st.text_input("Date", value="2018-07-07 22:09:11")

    text = st.text_area(
        "Review Text",
        value="If you decide to eat here, just be aware it is going to take about 2 hours...",
        height=160,
    )

    submitted = st.form_submit_button("Register Review")

if submitted:
    payload = {
        "review_id": review_id,
        "user_id": user_id,
        "business_id": business_id,
        "stars": stars,
        "useful": useful,
        "funny": funny,
        "cool": cool,
        "text": text,
        "date": date,
    }

    try:
        response = requests.post(REVIEW_REGISTER_URL, json=payload, timeout=10)
        response.raise_for_status()
        st.success("Review stored successfully.")
        st.json(response.json())
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")

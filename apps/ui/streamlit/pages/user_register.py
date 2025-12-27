import os

import requests
import streamlit as st


SERVING_API_URL = os.getenv("SERVING_API_URL", "http://backend-serving-api:8010/api")
USER_REGISTER_URL = f"{SERVING_API_URL.rstrip('/')}/users"

st.title("Register User")
st.write("Create or update a user record in MongoDB via the serving API.")

with st.form("user_register_form"):
    col1, col2 = st.columns(2)
    with col1:
        user_id = st.text_input("User ID", value="test-user-001")
        name = st.text_input("Name", value="Test User")
        yelping_since = st.text_input("Yelping Since", value="2020-01-01")
        review_count = st.number_input("Review Count", value=0, min_value=0, step=1)
        average_stars = st.number_input("Average Stars", value=0.0, min_value=0.0, max_value=5.0, step=0.1)
        fans = st.number_input("Fans", value=0, min_value=0, step=1)
    with col2:
        useful = st.number_input("Useful", value=0, min_value=0, step=1, key="metric_useful")
        funny = st.number_input("Funny", value=0, min_value=0, step=1, key="metric_funny")
        cool = st.number_input("Cool", value=0, min_value=0, step=1, key="metric_cool")
        friends = st.text_input("Friends (comma-separated)", value="")
        elite = st.text_input("Elite Years (comma-separated)", value="")

    st.subheader("Compliments")
    col3, col4 = st.columns(2)
    with col3:
        compliment_hot = st.number_input("Hot", value=0, min_value=0, step=1, key="compliment_hot")
        compliment_more = st.number_input("More", value=0, min_value=0, step=1, key="compliment_more")
        compliment_profile = st.number_input("Profile", value=0, min_value=0, step=1, key="compliment_profile")
        compliment_cute = st.number_input("Cute", value=0, min_value=0, step=1, key="compliment_cute")
        compliment_list = st.number_input("List", value=0, min_value=0, step=1, key="compliment_list")
        compliment_note = st.number_input("Note", value=0, min_value=0, step=1, key="compliment_note")
    with col4:
        compliment_plain = st.number_input("Plain", value=0, min_value=0, step=1, key="compliment_plain")
        compliment_cool = st.number_input("Cool", value=0, min_value=0, step=1, key="compliment_cool")
        compliment_funny = st.number_input("Funny", value=0, min_value=0, step=1, key="compliment_funny")
        compliment_writer = st.number_input("Writer", value=0, min_value=0, step=1, key="compliment_writer")
        compliment_photos = st.number_input("Photos", value=0, min_value=0, step=1, key="compliment_photos")

    submitted = st.form_submit_button("Register User")

if submitted:
    payload = {
        "user_id": user_id,
        "name": name,
        "review_count": review_count,
        "yelping_since": yelping_since,
        "useful": useful,
        "funny": funny,
        "cool": cool,
        "fans": fans,
        "average_stars": average_stars,
        "friends": friends,
        "elite": elite,
        "compliment_hot": compliment_hot,
        "compliment_more": compliment_more,
        "compliment_profile": compliment_profile,
        "compliment_cute": compliment_cute,
        "compliment_list": compliment_list,
        "compliment_note": compliment_note,
        "compliment_plain": compliment_plain,
        "compliment_cool": compliment_cool,
        "compliment_funny": compliment_funny,
        "compliment_writer": compliment_writer,
        "compliment_photos": compliment_photos,
    }

    try:
        response = requests.post(USER_REGISTER_URL, json=payload, timeout=10)
        response.raise_for_status()
        st.success("User stored successfully.")
        st.json(response.json())
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")

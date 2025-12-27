import json
import os

import requests
import streamlit as st


SERVING_API_URL = os.getenv("SERVING_API_URL", "http://backend-serving-api:8010/api")
BUSINESS_REGISTER_URL = f"{SERVING_API_URL.rstrip('/')}/businesses"

st.title("Register Business")
st.write("Create or update a business record in MongoDB via the serving API.")

with st.form("business_register_form"):
    col1, col2 = st.columns(2)
    with col1:
        business_id = st.text_input("Business ID", value="8wGISYjYkE2tSqn3cDMu8A")
        name = st.text_input("Name", value="Nifty Car Rental")
        address = st.text_input("Address", value="1241 Airline Dr")
        city = st.text_input("City", value="Kenner")
        state = st.text_input("State", value="LA")
        postal_code = st.text_input("Postal Code", value="70062")
    with col2:
        latitude = st.number_input("Latitude", value=29.981183, format="%.6f")
        longitude = st.number_input("Longitude", value=-90.254012, format="%.6f")
        stars = st.number_input("Stars", value=3.5, min_value=0.0, max_value=5.0, step=0.1)
        review_count = st.number_input("Review Count", value=14, min_value=0, step=1)
        is_open = st.selectbox("Is Open", options=[1, 0], index=0)

    categories = st.text_input(
        "Categories (comma-separated)",
        value="Automotive, Car Rental, Hotels & Travel, Truck Rental",
    )
    attributes_raw = st.text_area(
        "Attributes JSON (optional)",
        value="{}",
        height=120,
        help="Provide a JSON object or leave {}.",
    )
    hours_raw = st.text_area(
        "Hours JSON (optional)",
        value='{"Monday":"8:0-17:0","Tuesday":"8:0-17:0","Wednesday":"8:0-17:0","Thursday":"8:0-17:0","Friday":"8:0-17:0","Saturday":"9:0-15:0","Sunday":"9:0-12:0"}',
        height=120,
        help="Provide a JSON object with day keys or leave {}.",
    )

    submitted = st.form_submit_button("Register Business")

if submitted:
    try:
        attributes = json.loads(attributes_raw) if attributes_raw.strip() else None
        if isinstance(attributes, dict) and not attributes:
            attributes = None
    except json.JSONDecodeError as exc:
        st.error("Attributes JSON is invalid.")
        st.code(str(exc))
        st.stop()

    try:
        hours = json.loads(hours_raw) if hours_raw.strip() else None
        if isinstance(hours, dict) and not hours:
            hours = None
    except json.JSONDecodeError as exc:
        st.error("Hours JSON is invalid.")
        st.code(str(exc))
        st.stop()

    payload = {
        "business_id": business_id,
        "name": name,
        "address": address,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "latitude": latitude,
        "longitude": longitude,
        "stars": stars,
        "review_count": review_count,
        "is_open": is_open,
        "attributes": attributes,
        "categories": categories,
        "hours": hours,
    }

    try:
        response = requests.post(BUSINESS_REGISTER_URL, json=payload, timeout=10)
        response.raise_for_status()
        st.success("Business stored successfully.")
        st.json(response.json())
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")

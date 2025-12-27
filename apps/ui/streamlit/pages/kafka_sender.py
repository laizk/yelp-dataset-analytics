import streamlit as st
import requests
import json

SERVING_API_URL = "http://backend-serving-api:8010/api/kafka/publish/business"
# ^ Change to your serving API container name + port

st.title("Kafka Business Publisher")

st.write("Paste your JSON payload below. This will be sent to FastAPI, which publishes to Kafka.")

# Multiline JSON textbox
json_input = st.text_area("JSON Payload", height=200, placeholder='{\n  "business_name": "Acme Corp",\n  "value": 100\n}')

if st.button("Send to Kafka"):
    if not json_input.strip():
        st.warning("Please enter a valid JSON object.")
    else:
        try:
            # Parse JSON
            payload = json.loads(json_input)

            # Send to FastAPI endpoint
            response = requests.post(
                SERVING_API_URL,
                json=payload,
                timeout=8
            )

            st.subheader("Response:")
            if response.status_code == 200:
                st.success("Message sent successfully!")
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}")
                st.text(response.text)

        except json.JSONDecodeError as e:
            st.error("Invalid JSON format.")
            st.code(str(e))

        except Exception as e:
            st.error("Failed to send request.")
            st.exception(e)

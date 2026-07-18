import os
import streamlit as st
import requests

# API_URL selon l'environnement
IN_K8S = os.getenv("IN_K8S", "false").lower() == "true"
API_URL = "http://fastapi-service:8000/analyze" if IN_K8S else "http://localhost:8000/analyze"

st.set_page_config(page_title="Sentiment Analysis App")

user_input = st.text_area("Enter text:")

if st.button("Analyze"):
    try:
        response = requests.post(API_URL, json={"text": user_input})
        response.raise_for_status()
        data = response.json()
        st.write(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")

st.set_page_config(page_title="Sentiment Analysis App", page_icon="🧠", layout="centered")

st.title("🧠 Sentiment Analysis App")
user_input = st.text_area("Enter text:")

if st.button("Analyze"):
    try:
        response = requests.post(API_URL, json={"text": user_input}, timeout=10)
        response.raise_for_status()

        data = response.json()
        result = data["result"]
        label = result["label"]
        score = result["score"]

        color = "gray"
        if "Positive" in label:
            color = "green"
        elif "Negative" in label:
            color = "red"

        st.markdown(
            f"<h3 style='color:{color};'>Sentiment: {label}</h3>"
            f"<p><b>Confidence:</b> {score:.2f}</p>",
            unsafe_allow_html=True
        )

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error connecting to API: {e}")

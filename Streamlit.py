import requests
import streamlit as st

API_URL = "http://localhost:8000"  # FastAPI URL

# ---- SESSION STATE ----
if "token" not in st.session_state:
    st.session_state["token"] = None

# ---- AUTH FUNCTIONS ----
def register_user(username, password):
    payload = {"username": username, "password": password}
    response = requests.post(f"{API_URL}/auth/register", json=payload)
    return response


def login_user(username, password):
    payload = {"username": username, "password": password}
    response = requests.post(f"{API_URL}/auth/login", data=payload)
    if response.status_code == 200:
        st.session_state["token"] = response.json()["access_token"]
    return response
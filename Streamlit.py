import requests
import streamlit as st

API_URL = "http://localhost:8000"  # FastAPI URL

# ---- SESSION STATE ----
if "token" not in st.session_state:
    st.session_state["token"] = None


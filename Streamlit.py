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

# ---- BOOK FUNCTIONS ----
def get_books():
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    return requests.get(f"{API_URL}/books/", headers=headers)


def create_book(data):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    return requests.post(f"{API_URL}/books/", json=data, headers=headers)


def update_book(book_id, data):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    return requests.put(f"{API_URL}/books/{book_id}", json=data, headers=headers)


def delete_book(book_id):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    return requests.delete(f"{API_URL}/books/{book_id}", headers=headers)
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

# ---- STREAMLIT UI ----

st.title("📘 Book Management App (FastAPI + Streamlit)")

menu = ["Login", "Register", "Books"]
choice = st.sidebar.selectbox("Menu", menu)

# --- REGISTER PAGE ---
if choice == "Register":
    st.subheader("Create an Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        response = register_user(username, password)

        if response.status_code == 200:
            st.success("Account created!")
        else:
            st.error(response.json().get("detail", "Something went wrong"))

# --- LOGIN PAGE ---
elif choice == "Login":
    st.subheader("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = login_user(username, password)

        if response.status_code == 200:
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

    if st.session_state["token"]:
        st.info("You are logged in ✔")

# LOAD BOOKS
    if st.button("Refresh Books"):
        res = get_books()
        if res.status_code == 200:
            st.session_state["books"] = res.json()
        else:
            st.error("Failed to load books")

    books = st.session_state.get("books", [])

# DISPLAY BOOKS
    if books:
        for book in books:
            st.write(f"### {book['title']}")
            st.write(f"Author: {book['author']}")
            st.write(f"Pages: {book['pages']}")
            st.write(f"Description: {book['description']}")
            st.write("---")
    else:
        st.info("No books found. Add one below.")

# CREATE BOOK FORM
    st.subheader("➕ Add New Book")

    new_title = st.text_input("Title")
    new_author = st.text_input("Author")
    new_pages = st.number_input("Pages", min_value=1)
    new_desc = st.text_area("Description")

    if st.button("Add Book"):
        data = {
            "title": new_title,
            "author": new_author,
            "pages": new_pages,
            "description": new_desc
        }
        res = create_book(data)

        if res.status_code == 200:
            st.success("Book added!")
        else:
            st.error(res.json())

    st.subheader("✏ Update or Delete a Book")

    book_id = st.number_input("Book ID", min_value=1)

    updated_title = st.text_input("New Title")
    updated_author = st.text_input("New Author")
    updated_pages = st.number_input("New Pages", min_value=1)
    updated_desc = st.text_area("New Description")

    if st.button("Update Book"):
        data = {
            "title": updated_title,
            "author": updated_author,
            "pages": updated_pages,
            "description": updated_desc
        }
        res = update_book(book_id, data)

        if res.status_code == 200:
            st.success("Book updated!")
        else:
            st.error(res.json())

    if st.button("Delete Book"):
        res = delete_book(book_id)
        if res.status_code == 200:
            st.success("Book deleted!")
        else:
            st.error("Failed to delete book")

import requests
import streamlit as st
from PIL import Image

# ---------------------------
# CONFIG
# ---------------------------
API_BASE = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(
    page_title="Library App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------
# SESSION STATE DEFAULTS
# ------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "token" not in st.session_state:
    st.session_state.token = None


# ------------------------------------
# DARK MODE CSS
# ------------------------------------
def apply_dark_mode():
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
                body { background-color: #1e1e1e; }
                .title { color: #f1f1f1 !important; }
                .subtitle { color: #bbbbbb !important; }
                .stButton>button {
                    background-color: #333333 !important;
                    color: white !important;
                }
                .card {
                    background-color: #2b2b2b !important;
                    color: white !important;
                    box-shadow: 0px 2px 8px rgba(255,255,255,0.05);
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body { background-color: #f5f7fa; }
                .card {
                    background-color: white;
                    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
                }
            </style>
        """, unsafe_allow_html=True)


apply_dark_mode()

# ---------------------------
# SIDEBAR NAVIGATION + TOOLS
# ---------------------------
logo=Image.open("ZachTechs.jpg")
st.sidebar.image(logo, width=150)
st.sidebar.title("📚 Library System")

pages = ["Login", "Register", "Books"]
choice = st.sidebar.selectbox("📌 Navigation", pages)

# Dark mode toggle
dark_mode_toggle = st.sidebar.checkbox("🌙 Dark mode", value=st.session_state.dark_mode)
if dark_mode_toggle != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_mode_toggle
    st.rerun()

# Logout button (visible only if logged in)
if st.session_state.token:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.token = None
        st.success("Logged out successfully.")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("FastAPI + Streamlit UI")
st.caption("© 2025 ZachTechs")


# ---------------------------
# LOGIN PAGE
# ---------------------------
if choice == "Login":
    st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Access your account</div>', unsafe_allow_html=True)

    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        res = requests.post(f"{API_BASE}/login", json={
            "username": username,
            "password": password
        })

        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials.")



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

st.caption("© 2025 ZachTechs")
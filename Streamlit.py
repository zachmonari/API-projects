import requests
import streamlit as st
from PIL import Image

# ---------------------------
# CONFIG
# ---------------------------
logo=Image.open("ZachTechs.jpg")
st.image(logo, width=150)
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
def logout():
    if st.session_state.token:
        if st.sidebar.button("🚪 Logout"):
            st.session_state.token = None
            st.success("Logged out successfully.")
            st.rerun()
logout()

st.sidebar.markdown("---")
st.sidebar.info("FastAPI + Streamlit UI")
st.sidebar.caption("© 2025 ZachTechs")


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
        res = requests.post(f"{API_BASE}/login", data={
            "username": username,
            "password": password
        })

        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

# ---------------------------
# REGISTER PAGE
# ---------------------------
elif choice == "Register":
    st.markdown('<div class="title">📝 Register</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Create your account</div>', unsafe_allow_html=True)

    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        submit = st.form_submit_button("Register")

    if submit:
        if password != confirm:
            st.error("Passwords do not match!")
        else:
            res = requests.post(f"{API_BASE}/register", json={
                "username": username,
                "password": password
            })

            if res.status_code == 200:
                st.success("Account created!")
            else:
                st.error("Registration failed. Username might be taken.")


# ---------------------------
# BOOKS PAGE (CRUD)
# ---------------------------
elif choice == "Books":
    st.markdown('<div class="title">📚 Books</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Manage your book collection</div>', unsafe_allow_html=True)

    if not st.session_state.token:
        st.warning("Please login first.")


    token = st.session_state.token
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch books
    import requests
    from requests.exceptions import RequestException

    # Fetch books
    try:
        response = requests.get(f"{API_BASE}/books", headers=headers)
        response.raise_for_status()  # raises an error for 4xx and 5xx responses
        books = response.json()
        st.table(books)

    except RequestException as e:
        st.error(f"Network error: {str(e)}")
        st.stop()

    except ValueError:
        st.error("Invalid JSON response from backend.")
        st.stop()

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.stop()



    # Add Book
    st.markdown("### ➕ Add Book")
    with st.form("add_book"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        pages = st.number_input("Pages", min_value=1)
        description = st.text_area("Description", "")
        submit = st.form_submit_button("Add")


    if submit:
        res = requests.post(f"{API_BASE}/books", json={
            "title": title,
            "author": author,
            "pages": pages,
            "description": description
        }, headers=headers)

        if res.status_code == 200:
            st.success("Book added!")
            st.rerun()
        else:
            st.error("Failed to add book.")

    # Delete Book
    st.markdown("### ❌ Delete Book")
    book_id = st.number_input("Book ID", min_value=1, step=1)
    if st.button("Delete"):
        res = requests.delete(f"{API_BASE}/books/{book_id}", headers=headers)
        if res.status_code == 200:
            st.success("Book deleted.")
            st.rerun()
        else:
            st.error("Deletion failed.")





st.caption("© 2025 ZachTechs")
import streamlit as st
import requests

# Function to toggle theme
def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.get("theme", "light") == "light" else "light"

# Initialize session state for output and theme
if "review_output" not in st.session_state:
    st.session_state.review_output = None
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Set the theme
theme = st.session_state.theme

# Apply the theme
theme_styles = {
    "dark": {
        "background": "#1E1E1E",
        "text": "#FFFFFF",
        "textarea_bg": "#2D2D2D",
        "textarea_text": "#FFFFFF",
        "placeholder": "#A0A0A0",
        "cursor": "white",
    },
    "light": {
        "background": "#FFFFFF",
        "text": "#000000",
        "textarea_bg": "#F0F0F0",
        "textarea_text": "#000000",
        "placeholder": "#808080",
        "cursor": "black",
    },
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {theme_styles[theme]["background"]};
        color: {theme_styles[theme]["text"]};
    }}
    .stTextArea textarea {{
        background-color: {theme_styles[theme]["textarea_bg"]};
        color: {theme_styles[theme]["textarea_text"]};
        caret-color: {theme_styles[theme]["cursor"]} !important;
    }}
    .stTextArea textarea::placeholder {{
        color: {theme_styles[theme]["placeholder"]} !important;
    }}
    .stSelectbox select {{
        background-color: {theme_styles[theme]["textarea_bg"]};
        color: {theme_styles[theme]["textarea_text"]};
    }}
    .stButton button {{
        background-color: transparent !important;
        border: 1px solid #4CAF50 !important;
        color: #4CAF50 !important;
        border-radius: 5px !important;
    }}
    .theme-toggle {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 24px !important;
        padding: 0 !important;
        color: inherit !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {theme_styles[theme]["text"]} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Theme toggle button on the main screen
col1, col2 = st.columns([10, 1])
with col2:
    st.button("🌙" if theme == "light" else "🌞", on_click=toggle_theme, key="theme-toggle", help="Toggle theme")

# Title
st.markdown("<h1 style='text-align: center;'>🚀 Code Reviewer AI</h1>", unsafe_allow_html=True)

# Code input
st.markdown("**💻 Your Code:**")
code = st.text_area("", "", placeholder="Paste your code here...", height=300, label_visibility="collapsed")

# Language selection
st.markdown("**🌐 Select Language:**")
language = st.selectbox("", ["Python 🐍", 
        "JavaScript 🟨", 
        "Java ☕", 
        "C 🖥️"], label_visibility="collapsed")

# Get Code Review button
if st.button("Get Code Review"):
    if not code.strip():
        st.error("Please provide some code to review.")
    else:
        with st.spinner("Getting Code Review..."):
            try:
                response = requests.post(
                    "http://localhost:5000/review",
                    json={"code": code, "language": language},
                )
                if response.status_code == 200:
                    st.session_state.review_output = response.json().get("review", "No review available.")
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error occurred.')}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display the review output if it exists
if st.session_state.review_output:
    st.markdown("## Code Review Report:")
    st.markdown(st.session_state.review_output)
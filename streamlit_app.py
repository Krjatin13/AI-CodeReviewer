import streamlit as st
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
        if "GOOGLE_API_KEY" in st.secrets:
            return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass
    if st.session_state.get("api_key"):
        return st.session_state["api_key"]
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

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

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    default_key = get_api_key() or ""
    api_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.get("api_key", default_key),
        type="password",
        placeholder="Paste your Gemini API key...",
        help="Optional if configured in Streamlit Secrets. Get a free key at https://aistudio.google.com/app/apikey"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input.strip()
    st.markdown("[🔑 Get a free Gemini API Key](https://aistudio.google.com/app/apikey)")

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
            handled = False
            # Option 1: Try Flask backend if configured in Streamlit Secrets
            if "API_URL" in st.secrets:
                try:
                    API_URL = st.secrets["API_URL"].rstrip("/")
                    response = requests.post(
                        f"{API_URL}/review",
                        json={
                            "code": code,
                            "language": language.split(" ")[0]
                        },
                        timeout=15
                    )
                    if response.status_code == 200:
                        st.session_state.review_output = response.json().get("review", "No review available.")
                        handled = True
                except Exception:
                    pass

            # Option 2: Direct Gemini review (default/standalone mode)
            if not handled:
                active_key = get_api_key()
                if not active_key:
                    st.warning("⚠️ **Gemini API Key Required**: Please enter your Gemini API Key in the left sidebar to review code.")
                else:
                    try:
                        genai.configure(api_key=active_key)
                        prompt = (
                            f"You are a highly skilled code reviewer. Review the following {language} code and provide suggestions, optimizations, "
                            f"and best practices. Format the response using markdown for clarity.\n\n"
                            f"### Code:\n```{language}\n{code}\n```\n\n### Review:"
                            f"do not use heading Code Review "
                        )

                        models_to_try = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash", "gemini-pro-latest"]
                        review_success = False
                        last_err = None
                        for model_name in models_to_try:
                            try:
                                model = genai.GenerativeModel(model_name)
                                gen_resp = model.generate_content(prompt)
                                if gen_resp and hasattr(gen_resp, "text"):
                                    st.session_state.review_output = gen_resp.text.strip()
                                    review_success = True
                                    break
                            except Exception as m_err:
                                last_err = m_err
                                continue

                        if not review_success:
                            if last_err:
                                st.error(f"Error occurred: {str(last_err)}")
                            else:
                                st.error("Failed to get review from Gemini.")
                    except Exception as direct_err:
                        st.error(f"An error occurred: {str(direct_err)}")

# Display the review output if it exists
if st.session_state.review_output:
    st.markdown("## Code Review Report:")
    st.markdown(st.session_state.review_output)

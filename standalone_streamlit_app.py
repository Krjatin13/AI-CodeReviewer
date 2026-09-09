import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("GEMINI_API_KEY is not set! Please add it to your environment variables.")

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
language = st.selectbox(
    "", 
    [
        "Python 🐍", 
        "JavaScript 🟨", 
        "Java ☕", 
        "C 🖥️"
    ], 
    label_visibility="collapsed"
)

# Get Code Review button
if st.button("Get Code Review"):
    if not code.strip():
        st.error("Please provide some code to review.")
    else:
        with st.spinner("Getting Code Review..."):
            try:
                # Define the prompt for Gemini
                prompt = (
                    f"You are a highly skilled code reviewer. Review the following {language} code and provide suggestions, optimizations, "
                    f"and best practices. Format the response using markdown for clarity.\n\n"
                    f"### Code:\n```{language}\n{code}\n```\n\n### Review:"
                    f"do not use heading Code Review "
                )

                # Generate review using Gemini
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(prompt)

                if response and hasattr(response, "text"):
                    st.session_state.review_output = response.text.strip()
                else:
                    st.error("Failed to get a proper review from Gemini.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display the review output if it exists
if st.session_state.review_output:
    st.markdown("## Code Review Report:")
    st.markdown(st.session_state.review_output)
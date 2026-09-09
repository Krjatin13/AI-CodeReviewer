# 🚀 Code Reviewer AI

Code Reviewer AI is an advanced code review and optimization tool powered by Google's Gemini API. It provides instant feedback on code quality, suggests improvements, and identifies potential issues. The project features a sleek UI with a dark/light theme toggle and runs as a Streamlit web app.

## 🌟 Features

- 📝 **Code Review:** Get detailed suggestions for code optimization, readability, and potential bugs.
- 🌗 **Dark/Light Theme:** Seamlessly switch between dark and light modes.
- 🌐 **Language Support:** Supports multiple programming languages like Python, Java, C++, and more.
- ⏳ **Loader Animation:** Displays a loading indicator while fetching code reviews.
- 🛠️ **Standalone & Flask-Integrated:**
  - **Standalone:** Runs independently without any Flask server.
  - **Flask-Integrated:** Version requiring a Flask backend for enhanced functionality.

## 📸 Screenshots

### Dark Mode
![image](https://github.com/user-attachments/assets/f790aa99-370e-448b-9c40-b726d48a491e)



### Light Mode
![image](https://github.com/user-attachments/assets/d0a9c797-0422-40e3-adc9-fdd0529afb1b)



## 🏗️ Project Structure

```
├── standalone_streamlit_app.py   # Standalone Streamlit app (no Flask required)
├── streamlit_app.py              # Streamlit app with Flask(app.py)
├── app.py                        # Flask backend (used by streamlit_app.py)
├── README.md                     # Project documentation
├── requirements.txt              # Dependencies
              
```

## 🚀 Installation & Usage

### 1. **Clone the Repository**

```bash
git clone https://github.com/rnxtremer/AI-CodeReviewer.git
cd AI-CodeReviewer
```

### 2. **Set Up Environment**

Make sure you have Python 3.8+ and the `gemini-api` package installed. Set your `GEMINI_API_KEY` as an environment variable.

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Run the Standalone Streamlit App**

```bash
streamlit run standalone_streamlit_app.py
```

### 5. **Run the Flask-Integrated Streamlit App**

Start Flask first:

```bash
python app.py
```

Then, launch Streamlit:

```bash
streamlit run streamlit_app.py
```

## 🌐 Deployment

The app can be deployed seamlessly on platforms like Streamlit Sharing, Hugging Face Spaces, or Heroku.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📞 Contact

For questions or suggestions, reach out via GitHub issues.

---

⭐ If you like this project, please give it a star on [GitHub](https://github.com/rnxtremer/AI-CodeReviewer)!


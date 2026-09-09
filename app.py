from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")  

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY is not set!")

app = Flask(__name__)
CORS(app, resources={r"/review": {"origins": "*"}})
@app.route('/review', methods=['POST'])
def review_code():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "")

    if not code or not language:
        return jsonify({"error": "Please provide code and language"}), 400

    # Define the prompt for Gemini
    prompt = (
        f"You are a highly skilled code reviewer. Review the following {language} code and provide suggestions, optimizations, "
        f"and best practices. Format the response using markdown for clarity.\n\n"
        f"### Code:\n```{language}\n{code}\n```\n\n### Review:"
    )

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            # Format the review response as markdown
            formatted_review = response.text.strip()
            return jsonify({"review": formatted_review})
        else:
            return jsonify({"error": "Failed to get a proper review from Gemini"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
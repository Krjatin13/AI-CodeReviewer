
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured!")

# Configure Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app, resources={r"/review": {"origins": "*"}})


@app.route("/review", methods=["POST"])
def review_code():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip()
    language = data.get("language", "").strip()

    if not code or not language:
        return jsonify({
            "error": "Please provide code and language"
        }), 400

    prompt = f"""
You are an expert code reviewer.

Review this {language} code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Code quality and best practices
4. Performance and optimization
5. Suggested corrected code

Explain each issue clearly. Use Markdown.

Code:
```{language}
{code}
```
"""

    try:
        response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)
        )

        review = (response.text or "").strip()

        if not review:
            return jsonify({
                "error": "Gemini returned an empty review."
            }), 502

        return jsonify({"review": review}), 200

    except Exception:
        app.logger.exception("Gemini code review failed")
        return jsonify({
            "error": "Code review failed. Check the server logs and Gemini API configuration."
        }), 502


if __name__ == "__main__":
    app.run(debug=False)

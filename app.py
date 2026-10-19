
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Set it in CMD or your .env file."
    )

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
app = Flask(__name__)
CORS(app, resources={r"/review": {"origins": "*"}})


@app.route("/review", methods=["POST"])
def review_code():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip()
    language = data.get("language", "").strip()

    if not code or not language:
        return jsonify({
            "error": "Please provide both code and language."
        }), 400

    prompt = f"""
You are an expert code reviewer.
Review this {language} code for:
1. Bugs and logic errors
2. Security vulnerabilities
3. Code quality and best practices
4. Performance improvements
5. Suggested corrected code

Explain issues clearly using Markdown.

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

        review = (response.text or "").strip()
        if not review:
            return jsonify({
                "error": "Gemini returned an empty review."
            }), 502

        return jsonify({"review": review}), 200

    except Exception:
        app.logger.exception("Gemini code review failed")
        return jsonify({
            "error": "Review failed. Check the server logs and Gemini model access."
        }), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

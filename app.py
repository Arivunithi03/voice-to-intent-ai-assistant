from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Create Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


# ===============================
# ROUTE 1: PROCESS (Intent Refine)
# ===============================
@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.get_json()
        print("Incoming data:", data)  # Debug

        if not data or "text" not in data:
            return jsonify({"error": "Invalid request body"}), 400

        text = data["text"]

        # Create professional optimization prompt
        instruction = f"""
Rewrite the following user request into a highly professional,
structured AI prompt suitable for enterprise use.

User Request:
{text}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=instruction
        )

        optimized_prompt = response.text

        return jsonify({
            "optimized_prompt": optimized_prompt
        })

    except Exception as e:
        print("PROCESS ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ===============================
# ROUTE 2: GENERATE (Final Output)
# ===============================
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        print("Generate data:", data)  # Debug

        if not data or "prompt" not in data:
            return jsonify({"error": "Invalid request body"}), 400

        prompt = data["prompt"]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        ai_response = response.text

        return jsonify({
            "ai_response": ai_response
        })

    except Exception as e:
        print("GENERATE ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ===============================
# ROOT ROUTE (Optional Health Check)
# ===============================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Assistant Backend Running 🚀"})


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)

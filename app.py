from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env variables
load_dotenv()

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please ask a question."})

    # System role instruction
    system_prompt = (
        "You are a Museum & Tourist Guide chatbot. "
        "Always provide clear, factual, and engaging answers about history, monuments, "
        "artifacts, and tourist sites. Be simple, helpful, and friendly."
    )

    try:
        # Try Gemini Flash first (fast + free)
        model = genai.GenerativeModel("models/gemini-flash-latest")
        response = model.generate_content([system_prompt, question])
        answer = response.text if hasattr(response, "text") else "No reply generated."
        return jsonify({"answer": answer})

    except Exception as e:
        # If Flash fails (quota/exceeded/etc.), try Pro
        try:
            model = genai.GenerativeModel("models/gemini-pro-latest")
            response = model.generate_content([system_prompt, question])
            answer = response.text if hasattr(response, "text") else "No reply generated."
            return jsonify({"answer": answer})
        except Exception as e2:
            # Final fallback: show error
            return jsonify({"answer": f"Error: {str(e2)}"})

if __name__ == "__main__":
    app.run(debug=True)

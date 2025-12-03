from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import json
import re

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not set. Set it before running the server.")
openai.api_key = OPENAI_API_KEY

# Small helper to try to parse JSON returned by model
def safe_parse_json(s):
    try:
        return json.loads(s)
    except Exception:
        # try to extract a JSON-looking substring
        m = re.search(r'(\{.*\})', s, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                return None
        return None

@app.route("/api/interview", methods=["POST"])
def interview():
    data = request.get_json() or {}
    question = data.get("question", "")
    answer = data.get("answer", "")
    time_taken = data.get("timeTaken", None)

    # Basic validation
    if not question or not answer:
        return jsonify({"error": "question and answer required"}), 400

    # Build prompt asking the LLM to evaluate and return JSON
    system_prompt = (
        "You are an expert technical interviewer and coach. Given a user's answer to an interview question, "
        "provide a clear evaluation and a numeric score (0-100) for overall quality and for sub-criteria "
        "clarity, conciseness, and structure. Also detect filler words and count them, and provide either a "
        "short written feedback paragraph, and a single follow-up question the interviewer could ask. "
        "Respond ONLY in JSON with keys: analysis, feedback, followup, and serverReply (serverReply may be a short paraphrase). "
        "The analysis should be an object with keys: score (int 0-100), clarity (0-100), conciseness (0-100), structure (0-100), fillers (int), words (int)."
    )

    user_prompt = f"Question: {question}\n\nCandidate answer: {answer}\n\nTime taken (s): {time_taken}\n\nReturn the JSON as instructed."

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ],
            max_tokens=500,
            temperature=0.2
        )
        text = resp["choices"][0]["message"]["content"].strip()
        parsed = safe_parse_json(text)
        if parsed:
            return jsonify(parsed)
        else:
            # Fallback: return raw text in serverReply
            return jsonify({"analysis":{}, "feedback": None, "followup": None, "serverReply": text})
    except Exception as e:
        return jsonify({"error": "backend_error", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

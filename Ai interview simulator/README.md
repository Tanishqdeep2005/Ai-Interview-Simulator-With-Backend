
# AI Interview Simulator — Frontend + Minimal Flask Backend

This package includes:
- `index.html` — frontend (updated to optionally call `/api/interview`).
- `app.py` — minimal Flask backend that proxies to OpenAI to evaluate answers and return JSON feedback.
- `requirements.txt` — Python dependencies.
- `.env.example` — example environment variables.

## Running locally (VS Code)

1. **Create a Python virtual environment** (recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set your OpenAI API key**
Create a file named `.env` (or set environment variable in your shell) with:
```
OPENAI_API_KEY=sk-...
```
**Important:** never commit your real key to version control.

4. **Run the Flask backend**
```bash
python app.py
```
By default the server listens on port 5000.

5. **Open the frontend**
Use VS Code Live Server or a static server to serve `index.html`. Example:
```bash
python -m http.server 8000
# then open http://localhost:8000/index.html
```
When you switch the frontend to **Real LLM** mode, it will POST to `http://localhost:5000/api/interview` (same machine). If your backend is on a different host or port, either proxy requests or update the fetch URL in `index.html`.

## Notes & Security
- Keep API keys server-side only; the backend in this repo is an example and not production hardened.
- The Flask app asks the LLM to return JSON; LLMs may occasionally return malformed output — the server has a fallback to return raw text.
- Model choice: `gpt-3.5-turbo` is used as a safe default. You can change the `model` field in `app.py`.

## Next steps
- Add authentication to the backend if you expose it publicly.
- Add rate-limiting, input sanitization, and stronger JSON parsing for robustness.

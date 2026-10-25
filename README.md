# HERShield AI
Privacy-first women's safety hackathon prototype for journey check-ins, explainable suspicious-message warnings, and user-controlled incident notes.

## Features
- Journey check-in timer (works while app is open; not a guaranteed background task).
- Simulated SOS button; no real alert or location is sent.
- Rule-based, explainable message warning score.
- Session-only incident journal with JSON export and delete controls.
- Privacy and limitations page.

## Run locally (VS Code)
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Create a virtual environment: `py -m venv .venv`
4. Activate on Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
5. Install: `python -m pip install -r requirements.txt`
6. Run: `streamlit run app.py`
7. Test: `python -m pytest`

## Deploy
Push this folder to GitHub. In Streamlit Community Cloud, connect the repo, select branch `main`, and set main file to `app.py`. Test the deployed link before submitting.

## Demo message
`URGENT: verify your account now at https://example.invalid and send your OTP`

## Limitations
This is not an emergency service. The warning score is heuristic, not a trained ML model or definitive verdict. Never enter real OTPs, passwords, contact details, or sensitive evidence in a public demo.

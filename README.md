# PerspectiveAI (starter project)

A beginner-friendly LangChain + Gemini + Streamlit app that turns user-provided project experiences and lessons into platform-specific content drafts.

## 1. Requirements
- Python 3.10+ (a recent Python version is recommended)
- A Google Gemini API key
- Internet access

## 2. Create and activate a virtual environment

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

## 3. Configure the API key
1. Copy `.env.example` to a new file named `.env`.
2. Replace the placeholder with your own API key.
3. Never share or commit `.env` to GitHub.

## 4. Run the app
```bash
streamlit run app.py
```
Streamlit will print a local address to open in your browser.

## 5. Try this example
"I built a small Arduino rain detection project. I had trouble understanding the sensor's digital output and servo wiring. I learned how a sensor reading can control an actuator. Help me share this learning journey."

The app may ask a follow-up question before drafting. Choose a platform, tone, language, and length in the sidebar.

## Notes
- This starter uses conversation history in Streamlit session state. It is not permanent memory; it may be lost when the session is reset.
- It creates drafts only. It does not publish to social media.
- Review every draft before posting and correct any detail that doesn't reflect your experience.
- If `gemini-2.5-flash` is unavailable to your API key, use a currently available model ID from the provider's documentation.
- API usage may incur charges depending on your provider/account terms.

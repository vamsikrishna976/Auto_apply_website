AutoApply Website (final bundle)
--------------------------------
Steps to run (Windows):

1. Copy .env.example -> .env and update resume paths and CHROME_PROFILE_DIR to your local values.
2. Activate the same venv where Selenium worked (or create a new one in backend).
   Example:
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
3. Install backend requirements:
     cd backend
     pip install -r requirements.txt
4. Start the backend:
     python app.py
5. Open http://127.0.0.1:5000 in your browser and use the dashboard.
Notes:
- Replace any simplified wrapper scripts in backend with your exact full scripts if you prefer.
- The naukri_page.html snapshot included is from your uploaded file.

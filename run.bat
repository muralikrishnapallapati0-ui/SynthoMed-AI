@echo off
echo ==========================================
echo Starting SynthoMed AI (Streamlit Native)
echo ==========================================
echo.

if not exist venv (
  echo [1/3] Creating Python virtual environment...
  py -m venv venv
)

echo [2/3] Activating environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt > nul

echo [3/3] Launching Streamlit Application...
echo The app will open in your default browser automatically.
echo (Do not close this window while using the app)
echo.

streamlit run app.py

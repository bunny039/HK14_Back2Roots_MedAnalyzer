@echo off
REM MediAssist Launcher for Windows

echo.
echo ════════════════════════════════════════════════════════════
echo   MediAssist - Medical Report Intelligence System
echo   Launching Streamlit App...
echo ════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Streamlit is not installed
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the app
echo Starting MediAssist...
echo Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause

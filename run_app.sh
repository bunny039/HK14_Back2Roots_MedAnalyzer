#!/bin/bash

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  MediAssist - Medical Report Intelligence System"
echo "  Launching Streamlit App..."
echo "════════════════════════════════════════════════════════════"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "ERROR: Streamlit is not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the app
echo "Starting MediAssist..."
echo "Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m streamlit run app.py

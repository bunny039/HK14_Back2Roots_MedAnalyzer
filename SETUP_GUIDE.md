# MediAssist - Complete Setup Guide

## 📋 Prerequisites

- Python 3.9 or higher
- pip package manager
- Tesseract OCR engine
- Poppler utilities
- Internet connection (for Gemini API)

## 🔧 Step-by-Step Installation

### Step 1: Install Python Dependencies

```bash
cd "c:\Users\bhoumik\Downloads\mediassist\files (1)"
pip install -r requirements.txt
```

This will install:
- **streamlit** - Web app framework
- **google-generativeai** - Gemini API client
- **google-auth-oauthlib** - Google Auth for Gmail API
- **google-api-python-client** - Google API Client
- **pandas** - Data handling
- **numpy** - Numerical computing
- **Pillow** - Image processing
- **pdfplumber** - PDF text extraction
- **pdf2image** - PDF to image conversion
- **pytesseract** - Tesseract OCR wrapper
- **opencv-python-headless** - Computer vision
- **gtts** - Text-to-speech

### Step 2: Install System OCR Dependencies

#### Windows:
```powershell
# Using Chocolatey
choco install tesseract poppler

# OR manual download:
# Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Poppler: https://github.com/oschwartz10612/poppler-windows/releases/
```

#### macOS:
```bash
brew install tesseract poppler
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

### Step 3: Configure Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set it as an environment variable:

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
```

**Windows Command Prompt:**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Persistent Setup (Windows):**
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Add new User variable:
   - Variable name: `GEMINI_API_KEY`
   - Variable value: your actual API key
5. Restart any terminals/IDE

**Persistent Setup (macOS/Linux):**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Step 4: Verify Installation

Run the dependency check:
```bash
python -c "
try:
    import streamlit; print('✓ Streamlit installed')
except: print('✗ Streamlit missing')
try:
    import google.generativeai; print('✓ Google Generative AI installed')
except: print('✗ Google Generative AI missing')
try:
    import pytesseract; print('✓ pytesseract installed')
except: print('✗ pytesseract missing')
try:
    import cv2; print('✓ OpenCV installed')
except: print('✗ OpenCV missing')
try:
    import pdfplumber; print('✓ pdfplumber installed')
except: print('✗ pdfplumber missing')
try:
    from gtts import gTTS; print('✓ gTTS installed')
except: print('✗ gTTS missing')
"
```

## 🚀 Running the Application

```bash
cd "c:\Users\bhoumik\Downloads\mediassist\files (1)"
streamlit run app.py
```

The application will start at: **http://localhost:8501**

## 📝 Usage Guide

### 1. Upload Report
- Click "Upload Report" in the sidebar
- Upload a PDF, JPG, or PNG file of your medical report
- Click "Analyse Report"

### 2. View Dashboard
- See extracted lab values
- View risk scores
- Chat with the AI assistant

### 3. Get Explanation
- Read personalised explanations
- View lifestyle suggestions
- Listen to audio summary

### 4. Doctor Mode
- View raw extracted text
- Export data as JSON/CSV
- Add clinical notes and verification

### 5. Settings
- Configure patient profile
- Check OCR dependencies
- Clear session data

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'gtts'"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: "Tesseract is not installed"
**Solution:** Install Tesseract OCR from the system dependencies section above

### Issue: "ERROR: Gemini API key not configured"
**Solution:** Set the `GEMINI_API_KEY` environment variable (see Step 3)

### Issue: "No module named 'streamlit'"
**Solution:** Run `pip install streamlit` or `pip install -r requirements.txt`

### Issue: "pdf2image ImportError"
**Solution:** Install poppler: `choco install poppler` (Windows) or `brew install poppler` (Mac)

### Issue: "OCR not working on scanned PDFs"
**Solution:** Install Tesseract: See Step 2 above

## 📦 File Structure

```
mediassist/
├── app.py                 # Main Streamlit app
├── styles.py              # CSS styling
├── ocr_utils.py          # OCR & text cleaning
├── extraction_utils.py   # Text parsing & risk scoring
├── chatbot_utils.py      # Gemini API integration
├── requirements.txt      # Python dependencies
├── README.md             # Overview
└── SETUP_GUIDE.md        # This file
```

## 🔐 Security Notes

- Never commit the `GEMINI_API_KEY` to version control
- Always use environment variables for sensitive data
- Do not hardcode API keys in source files
- The hardcoded API key in chatbot_utils.py has been removed

## 📚 Documentation

- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Generative AI](https://ai.google.dev/)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- [PDF Plumber](https://github.com/jsvine/pdfplumber)

## 🆘 Support

If you encounter issues:
1. Check the error message carefully
2. Verify all dependencies are installed
3. Ensure Gemini API key is set correctly
4. Clear browser cache: Ctrl+Shift+Delete
5. Restart Streamlit: Press `Ctrl+C` and run again

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] All pip packages installed (`pip install -r requirements.txt`)
- [ ] Tesseract OCR installed
- [ ] Poppler installed
- [ ] Gemini API key set as environment variable
- [ ] `streamlit run app.py` starts without errors
- [ ] App opens at http://localhost:8501
- [ ] Can upload a test medical report PDF
- [ ] Chat with AI assistant works (with API key set)

---

**Last Updated:** February 22, 2026
**Version:** 2.0

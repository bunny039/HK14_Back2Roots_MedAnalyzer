# 🏥 MedAnalyzer — Medical Report Intelligence System

> A production-grade, AI-powered medical report analysis tool built with Streamlit.

---
## Collaborately Made By Team Back2Roots
> Bhoumik Choudhury <br>
> Sameer Ranjan Nayak <br>
> Pritish Behera <br>
> Gudla Vivek <br>

---
## 🔁 Full Pipeline

```
User Uploads Report
        ↓
Stage 1: OCR Engine          (pdfplumber / pdf2image + OpenCV + Tesseract)
        ↓
Stage 2: Text Cleaning       (normalise, strip noise, OCR correction)
        ↓
Stage 3: Structured Extraction  (regex + 60+ test reference database)
        ↓
Stage 4: Abnormal Detection Engine  (Low / Normal / High + severity)
        ↓
Stage 5: Risk Scoring Layer     (Diabetes, Cardio, Kidney, Liver, Thyroid, Anaemia)
        ↓
Stage 6: Personalised Explanation Generator  (plain language, age-aware)
        ↓
Stage 7: Doctor Verification Mode  (raw text, JSON, CSV export)
        ↓
Stage 8: Chatbot Interaction Layer  (Gemini API + rule-based fallback)
        ↓
Stage 9: Final Dashboard Display   (hero card, lab table, risk chart, chat)
```

---

## 📁 File Structure

```
mediassist/
├── app.py              # Main app — router, pages, pipeline runner, UI components
├── styles.py           # All CSS (Fraunces + Syne fonts, dark sidebar, card system)
├── ocr_utils.py        # Stages 1 & 2: OCR engine + text cleaning
├── extraction_utils.py # Stages 3–6: extraction, detection, risk scoring, explanation
├── chatbot_utils.py    # Stage 8: Gemini API chatbot + rule-based fallback
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Install system dependencies (for OCR)

**Windows (using WSL or git bash):**
```bash
# Install Tesseract
choco install tesseract  # or using scoop or manual install

# Install Poppler (for pdf2image)
choco install poppler
```

**macOS:**
```bash
brew install tesseract
brew install poppler
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### 3. Set up Gemini API Key

Get your API key from [Google AI](https://makersuite.google.com/app/apikey), then set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_actual_api_key_here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

**macOS/Linux:**
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

Or create a `.env` file (and the app will load it if using python-dotenv).

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🚀 Full Pipeline

```bash
pip install -r requirements.txt
```

### 2. Install system dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**
- Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Poppler: https://github.com/oschwartz10612/poppler-windows

### 3. Set Gemini API key (optional — enables full Gemini AI chat)

```bash
export GEMINI_API_KEY=your_key_here
```

Without this, the app uses a smart rule-based chatbot automatically.

### 4. Run

```bash
cd mediassist
streamlit run app.py
```

---

## 🗺️ Navigation

| Page | What it does |
|---|---|
| **Dashboard** | Hero summary, colour-coded lab table, risk analysis, AI chat |
| **Upload Report** | File upload, full pipeline execution with progress, preview |
| **Explanation** | Per-finding explanations + personalised lifestyle tips |
| **Doctor Mode** | Raw text, structured JSON/CSV export, risk detail (requires toggle) |
| **Settings** | Patient profile, API key status, OCR dependencies, session reset |

---

## 🩺 Doctor Mode

Toggle **Doctor Mode** in the sidebar to access:
- Raw OCR-extracted text
- Cleaned text diff
- Structured DataFrame
- JSON + CSV export
- Risk score breakdown with clinical insights

---

## 🔒 Safety Design

- **No diagnosis** — the system never tells users they "have" a condition
- **No prescription** — no medication names or dosages are suggested
- **Grounded responses** — chatbot only discusses values present in the report
- **Disclaimer always shown** — on every summary and explanation view
- **Senior-friendly** — if age ≥ 60, simpler language is used throughout

---

## 📋 Disclaimer

MediAssist is for **informational and educational purposes only**.
It does not constitute medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional for health decisions.

# MediAssist - Comprehensive Guide

## ✨ Features

### 🏥 Medical Report Analysis
- **OCR Engine**: Extracts text from PDFs, scanned documents, and images
- **Text Cleaning**: Removes noise and normalizes extracted text
- **Lab Parameter Extraction**: Identifies 100+ different lab tests
- **Abnormal Detection**: Flags values outside normal ranges
- **Risk Scoring**: Calculates health risks across 6 categories

### 🤖 AI-Powered Insights
- **Gemini Integration**: Uses Google's advanced AI for explanations
- **Adaptive Complexity**: Automatically adjusts explanation detail based on user questions
- **Multi-Language Support**: Responds in multiple languages
- **Plain Language**: Explains medical terms in simple language

### 📊 Doctor Verification Mode
- **Raw Data Export**: Download extracted text, JSON, and CSV
- **Digital Signatures**: Add doctor verification
- **Prescription Management**: Record recommended medications
- **Clinical Notes**: Document physician observations

### 🔊 Accessibility
- **Text-to-Speech**: Listen to reports and explanations
- **Voice Summary**: Audio versions of key findings
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🎯 Supported Lab Tests (100+)

### Blood Testing
- **Hematology**: Hemoglobin, WBC, RBC, Platelets, Hematocrit, MCV, MCH
- **Glucose**: Fasting/Random Blood Sugar, HbA1c
- **Lipids**: Total Cholesterol, LDL, HDL, Triglycerides
- **Liver Function**: AST, ALT, ALP, Bilirubin, Albumin
- **Kidney Function**: Creatinine, BUN, Uric Acid, eGFR
- **Thyroid**: TSH, Free T3, Free T4
- **Electrolytes**: Sodium, Potassium, Calcium, Magnesium
- **Others**: Iron, Ferritin, Vitamin B12, Folate, CRP, PSA, hCG

## 🚀 Getting Started

### Quick Start (5 minutes)

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Gemini API Key:**
   ```powershell
   $env:GEMINI_API_KEY = "your_key_here"
   ```

3. **Run the App:**
   ```bash
   streamlit run app.py
   ```

4. **Upload a Medical Report:**
   - Click "Upload Report"
   - Select a PDF, JPG, or PNG file
   - Click "Analyse Report"

5. **View Results:**
   - Go to "Dashboard" to see your lab results
   - Click "Explanation" for insights
   - Use "Chat" to ask questions about your results

### Full Setup (30 minutes)

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation instructions.

## 🎓 Understanding the Results

### Lab Results Table
- **Test Name**: The medical test (e.g., Blood Glucose)
- **Value**: Your actual result
- **Unit**: The measurement unit (e.g., mg/dL)
- **Reference Range**: Normal values for comparison
- **Status**: Normal / High / Low flag
- **Severity**: Mild / Moderate / Severe (if abnormal)

### Risk Categories

#### 🩸 Diabetes Risk
- **Tests**: Glucose, HbA1c, Blood Sugar
- **What it means**: Indicates glucose control and diabetes risk
- **Lifestyle**: Exercise, diet, weight management

#### ❤️ Cardiovascular Risk
- **Tests**: Cholesterol, LDL, HDL, Triglycerides
- **What it means**: Heart disease risk factors
- **Lifestyle**: Reduce saturated fats, increase exercise

#### 🫘 Kidney Function
- **Tests**: Creatinine, BUN, Uric Acid, eGFR
- **What it means**: How well your kidneys filter waste
- **Lifestyle**: Stay hydrated, limit salt, monitor protein

#### 🫀 Liver Function
- **Tests**: AST, ALT, Alkaline Phosphatase, Bilirubin
- **What it means**: Liver health and function
- **Lifestyle**: Limit alcohol, maintain healthy weight

#### 🦋 Thyroid Health
- **Tests**: TSH, Free T3, Free T4
- **What it means**: Thyroid hormone regulation
- **Lifestyle**: Sleep, stress management, medication adherence

#### 💉 Anemia Risk
- **Tests**: Hemoglobin, Red Blood Cells, Hematocrit, Iron
- **What it means**: Oxygen-carrying capacity of blood
- **Lifestyle**: Iron-rich diet, B12 sources, supplements if needed

## 💬 Chat Examples

### Simple Questions
- "Is my sugar high?"
- "What does this mean?"
- "Am I sick?"

**Response**: Direct, reassuring answer using simple language

### Detailed Questions
- "Explain why my WBC is high"
- "What are the implications of elevated creatinine?"
- "What causes HbA1c elevation?"

**Response**: Detailed explanation with medical context

## 🔐 Privacy & Security

- **Local Processing**: Initial OCR runs locally on your machine
- **API Usage**: Medical data sent only to Gemini API when you ask questions
- **No Data Storage**: Results not stored on servers (only in your session)
- **Environment Variables**: API key never committed to code
- **Encrypted**: Use HTTPS connection (use ngrok or deployment service)

## ⚙️ Customization

### Change Colors
Edit `styles.py`:
```python
--blue: #NEW_COLOR;
--green: #NEW_COLOR;
```

### Add More Lab Tests
Edit `extraction_utils.py` - `REFERENCE_DB` dictionary

### Modify Risk Categories
Edit `extraction_utils.py` - `RISK_CATEGORIES` dictionary

### Adjust AI Prompts
Edit `chatbot_utils.py` - `_SYSTEM_PROMPT` variable

## 🐛 Common Issues & Solutions

### 1. "No module named 'streamlit'"
```bash
pip install streamlit
```

### 2. "Tesseract is not installed"
- **Windows**: `choco install tesseract`
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

### 3. "PDF extraction not working"
- Install Poppler: `choco install poppler`
- Ensure file is readable and not corrupted
- Try image-based OCR instead

### 4. "API key error"
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your_key"

# Verify it's set
$env:GEMINI_API_KEY
```

### 5. "Out of memory" on large PDF
- Try a smaller PDF file first
- Increase Python heap size:
  ```bash
  python -Xmx2g -m streamlit run app.py
  ```

### 6. "Chat not working"
- Verify Gemini API key is set
- Check internet connection
- Ensure rate limits not exceeded
- Try asking a simpler question

## 📈 Performance Tips

1. **Faster OCR**: Use text-based PDFs when possible (pdfplumber is 10x faster)
2. **Reduce File Size**: Compress PDFs before uploading
3. **Cache Results**: Session state keeps data in memory
4. **Parallel Processing**: Results display as each stage completes

## 📚 For Developers

### Adding New Features

1. **New Lab Tests**: Update `REFERENCE_DB` in `extraction_utils.py`
2. **New Risk Categories**: Add to `RISK_CATEGORIES` in `extraction_utils.py`
3. **AI Customization**: Modify `_SYSTEM_PROMPT` in `chatbot_utils.py`
4. **UI Changes**: Edit relevant component in `app.py`

### Project Structure
```
app.py                    # Main Streamlit app (1,255 lines)
├── Session state init
├── Navigation & sidebar
├── Page renderers
│   ├── page_dashboard()
│   ├── page_upload()
│   ├── page_explanation()
│   ├── page_doctor_mode()
│   └── page_settings()
└── Pipeline runner

styles.py                 # CSS styling (736 lines)
├── Design tokens
├── Component styles
└── Dark theme

ocr_utils.py             # Stage 1-2 (255 lines)
├── OCR extraction
├── Image preprocessing
├── Text cleaning
└── Dependency checking

extraction_utils.py      # Stage 3-6 (653 lines)
├── Parameter extraction
├── Abnormal detection
├── Risk scoring
└── Explanation generation

chatbot_utils.py        # Stage 8 (121 lines)
├── Gemini API integration
├── Context building
└── Response generation
```

### Testing

1. **Unit Tests**: Add to `tests/` directory
2. **Sample Data**: Use `samples/` folder with test PDFs
3. **Manual Testing**: Upload test medical reports

## 🌍 Deployment

### Streamlit Cloud (Easiest)
```bash
git push origin main
# Then deploy from https://share.streamlit.io/
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Azure/AWS/GCP
Follow platform-specific Streamlit deployment guides

## 📞 Support & Feedback

- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for troubleshooting
- Review error messages carefully
- Clear cache: `Ctrl+Shift+Delete`
- Restart app: `Ctrl+C` then `streamlit run app.py`

## ⚖️ Legal Disclaimer

**MediAssist is for informational purposes only.**

- **NOT a medical device**
- Results should be verified by healthcare professionals
- Always consult with a qualified doctor before making health decisions
- Keep records of analyses for your physician
- Use current medical guidelines, not historical standards

## 📄 License

This project is provided as-is for educational and research purposes.

---

**Created**: February 2026
**Version**: 2.0
**Status**: Production Ready ✅

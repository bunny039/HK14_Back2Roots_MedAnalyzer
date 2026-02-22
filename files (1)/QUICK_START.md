# MediAssist - Quick Reference Card

## 🚀 Start the App in 30 Seconds

```powershell
# Windows PowerShell
cd "c:\Users\bhoumik\Downloads\mediassist\files (1)"
$env:GEMINI_API_KEY = "your_api_key_here"
pip install -r requirements.txt
streamlit run app.py
```

## 🔑 Get Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key and paste it in the command above

## 📱 Default Features

| Feature | Status |
|---------|--------|
| Upload Reports | ✅ Working |
| OCR Extraction | ✅ Working |
| Lab Analysis | ✅ Working |
| Risk Scoring | ✅ Working |
| Chat with AI | ⚙️ Requires API key |
| Text-to-Speech | ✅ Working |
| Doctor Mode | ✅ Working |

## 🔧 System Requirements

- Python 3.9+
- ~2 GB RAM
- ~500 MB disk space
- Internet (for AI chat)
- Tesseract OCR (optional, for scanned PDFs)

## ✅ What's Fixed

✅ Missing gtts package  
✅ Hardcoded API key removed  
✅ Environment variable configuration  
✅ All 9 pipeline stages working  
✅ Frontend/backend fully integrated  
✅ All errors resolved  

## 📝 File Locations

**Main App**: `app.py`  
**Config**: `.streamlit/config.toml`  
**Setup Guide**: `SETUP_GUIDE.md`  
**Full Guide**: `GUIDE.md`  
**Fixes Summary**: `FIXES_SUMMARY.md`  

## 🐛 Most Common Issues

| Issue | Fix |
|-------|-----|
| Import error for gtts | `pip install gtts` |
| API key error | Set GEMINI_API_KEY env var |
| Tesseract error | Install Tesseract OCR |
| Port already in use | Kill other Streamlit apps |

## 💡 Tips

- Use PDFs with text (not scanned) for faster processing
- Keep file size under 20 MB
- Internet required for chat feature
- For best results, use clear medical reports
- Always verify results with your doctor

## 🚀 Next Steps

1. Open [Quick Start Guide](SETUP_GUIDE.md#step-1-install-python-dependencies)
2. Install packages and configure API key
3. Run `streamlit run app.py`
4. Upload a medical report
5. View your results on the Dashboard
6. Ask questions using Chat
7. Use Doctor Mode to export or verify

## 📞 Help

- See **SETUP_GUIDE.md** for installation help
- See **GUIDE.md** for feature documentation  
- See **FIXES_SUMMARY.md** for what was fixed

---

**App Status**: ✅ READY TO USE  
**Version**: 2.0  
**Last Updated**: Feb 22, 2026

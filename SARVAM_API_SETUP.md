# Sarvam AI API Setup Guide

## ✨ High-Quality Indian Language Voice Support

MediAssist now uses **Sarvam AI** for text-to-speech, providing superior audio quality for all 10 Indian languages!

## 📋 Quick Setup

### Step 1: Get Sarvam API Key
1. Visit: **https://www.sarvam.ai/**
2. Sign up for a free account
3. Go to your **API Dashboard**
4. Copy your **API Key**

### Step 2: Set Environment Variable (Windows PowerShell)
```powershell
$env:SARVAM_API_KEY = "your_sarvam_api_key_here"
```

### Step 3: Launch App
```powershell
cd "c:\Users\bhoumik\Downloads\mediassist\files (1)"
streamlit run app.py
```

### Step 4: Verify Setup
- Open sidebar: **🔊 Voice & Language**
- Check API Status indicator
- ✅ Shows "✅ Configured" if key is set
- ❌ Shows "❌ Not Set" if key is missing

---

## 🗣️ Supported Languages

### 10 Indian Languages 🇮🇳
- **Hindi** (hi-IN) - हिंदी
- **Tamil** (ta-IN) - தமிழ்
- **Telugu** (te-IN) - తెలుగు
- **Kannada** (kn-IN) - ಕನ್ನಡ
- **Malayalam** (ml-IN) - മലയാളം
- **Marathi** (mr-IN) - मराठी
- **Gujarati** (gu-IN) - ગુજરાતી
- **Bengali** (bn-IN) - বাংলা
- **Punjabi** (pa-IN) - ਪੰਜਾਬੀ
- **Urdu** (ur-IN) - اردو

### International Languages
- English (en-US) 🇬🇧
- Spanish (es-ES) 🇪🇸
- French (fr-FR) 🇫🇷
- German (de-DE) 🇩🇪
- Chinese (zh-CN) 🇨🇳
- Japanese (ja-JP) 🇯🇵

---

## 🎵 Using Voice Features

1. **Select Language** from sidebar dropdown
2. **Click Play Audio** button on any page:
   - Dashboard → "Play Summary Audio"
   - Chat → "Play Answer Audio"
   - Explanation → "Play Explanation Audio"
   - Doctor Mode → "Play Raw Text Audio"
3. **Listen** to audio in your selected language! 🔊

---

## 🔧 Sarvam API Features Used

| Setting | Value | Purpose |
|---------|-------|---------|
| Speaker | "meera" | Natural Indian voice |
| Pitch | 1.0 | Natural pitch |
| Pace | 1.0 | Normal speaking speed |
| Loudness | 1.5 | Clear audio output |

---

## 💡 Why Sarvam AI?

✅ **Superior Indian Language Support** - Native speakers quality
✅ **Cloud-Based** - No local installation needed
✅ **High Quality** - Professional audio output
✅ **Fast** - Real-time TTS generation
✅ **Free Tier** - Get started immediately
✅ **Scalable** - Handle production loads

---

## ⚡ Quick Troubleshooting

### Audio not playing?
1. Check SARVAM_API_KEY is set
2. Verify API key is valid on sarvam.ai
3. Check internet connection
4. Try refreshing page (F5)

### Wrong language playing?
1. Confirm language is selected in sidebar
2. Check API Status shows ✅ Configured
3. Try selecting a different language
4. Restart app if language doesn't update

### API Key not recognized?
1. Double-check key is copied correctly
2. Remove extra spaces from key
3. Verify key is active on sarvam.ai dashboard
4. Try generating a new API key

---

## 📞 Support

- **Sarvam AI Docs**: https://docs.sarvam.ai/
- **API Status**: Check sidebar indicator
- **Report Issues**: Check app logs in terminal

---

## 🚀 Start Using

**Set your API key now:**
```powershell
$env:SARVAM_API_KEY = "your_api_key_here"
```

**Then run:**
```powershell
streamlit run app.py
```

Enjoy crystal-clear audio in any of 10 Indian languages! 🇮🇳🎵


"""
app.py — MediAssist: Medical Report Intelligence System
════════════════════════════════════════════════════════
Full pipeline:
  Stage 1: OCR Engine
  Stage 2: Text Cleaning
  Stage 3: Structured Extraction
  Stage 4: Abnormal Detection Engine
  Stage 5: Risk Scoring Layer
  Stage 6: Personalised Explanation Generator
  Stage 7: Doctor Verification Mode
  Stage 8: Chatbot Interaction Layer
  Stage 9: Final Dashboard Display
"""

import streamlit as st
import pandas as pd
import json
import os
import io
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


# ── Page config (must be FIRST Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="MediAssist — Medical Report Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Local modules ─────────────────────────────────────────────────────────────
from styles import MAIN_CSS
from ocr_utils import extract_text, clean_text, get_dependency_status
from extraction_utils import (
    extract_parameters,
    detect_abnormal,
    compute_risk_scores,
    generate_summary,
)
from chatbot_utils import chatbot_response

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(MAIN_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════

def _init_state():
    defaults = {
        "page":         "Dashboard",
        "raw_text":     "",
        "ocr_method":   "",
        "cleaned_text": "",
        "df":           pd.DataFrame(),
        "summary":      {},
        "risk_scores":  [],
        "chat_history": [],
        "doctor_mode":  False,
        "report_ready": False,
        "patient_age":  35,
        "patient_gender": "Not specified",
        # Pipeline stage tracker
        "stage": 0,
        # Doctor Verification & Therapeutics (Enhanced)
        "doctor_notes": "",
        "prescriptions": [],
        "doctor_verified": False,
        "doctor_name": "",
        "doctor_license": "",
        "doctor_hospital": "",
        "verification_timestamp": None,
        "digital_signature": "",
        # Enhanced Doctor Mode Features
        "diagnosis_notes": "",
        "follow_up_date": None,
        "urgency_level": "Normal",
        "lab_interpretations": "",
        "referral_specialists": [],
        "test_recommendations": [],
        "contraindications": "",
        "patient_allergies": "",
        # Voice & Language Settings
        "voice_language": "English",
        # API Key storage
        "api_key": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ══════════════════════════════════════════════════════════════════════
# LANGUAGE SUPPORT - VOICE & TTS
# ══════════════════════════════════════════════════════════════════════

# Language codes for gTTS support (including 10 Indian languages)
LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
}

# Language to ISO 639-1 code mapping for IndicTrans2
LANG_TO_ISO = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "ta": "tam_Tamil",
    "te": "tel_Telu",
    "kn": "kan_Knda",
    "ml": "mal_Mlym",
    "mr": "mar_Deva",
    "gu": "guj_Gujr",
    "bn": "ben_Beng",
    "pa": "pan_Guru",
    "ur": "urd_Arab",
    "es": "spa_Latn",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "zh-CN": "zho_Hans",
    "ja": "jpn_Jpan",
}

# ══════════════════════════════════════════════════════════════════════
# TRANSLATION FUNCTION (Google Translate API)
# ══════════════════════════════════════════════════════════════════════

def translate_to_language(text: str, target_lang: str) -> str:
    """
    Translate text to target language using multiple reliable methods.
    
    Supports translation to:
    - 10 Indian languages (Hindi, Tamil, Telugu, Kannada, Malayalam, etc.)
    - English, Spanish, French, German, Chinese, Japanese
    """
    if not text or not text.strip():
        return ""
    
    # If already in English, return as is
    if target_lang == "en":
        return text
    
    # Language code mapping for Google Translate
    lang_map = {
        "en": "en",
        "hi": "hi",
        "ta": "ta",
        "te": "te",
        "kn": "kn",
        "ml": "ml",
        "mr": "mr",
        "gu": "gu",
        "bn": "bn",
        "pa": "pa",
        "ur": "ur",
        "es": "es",
        "fr": "fr",
        "de": "de",
        "zh-CN": "zh-CN",
        "ja": "ja",
    }
    
    target_lang_code = lang_map.get(target_lang, "en")
    
    if target_lang_code == "en":
        return text
    
    try:
        # Truncate if too long
        text_to_translate = text[:500] if len(text) > 500 else text
        
        # Use Google Translate API (free, no key required)
        translate_url = "https://translate.google.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": target_lang_code,
            "dt": "t",
            "q": text_to_translate
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        response = requests.get(translate_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result and isinstance(result, list) and len(result) > 0:
                # Extract translation from response
                translation_parts = []
                try:
                    for item in result[0]:
                        if isinstance(item, list) and len(item) > 0:
                            part = str(item[0])
                            if part:
                                translation_parts.append(part)
                except:
                    pass
                
                translated = "".join(translation_parts).strip()
                if translated and len(translated) > 0:
                    return translated
    
    except Exception as e:
        pass
    
    # If translation fails, return original text
    return text

# ══════════════════════════════════════════════════════════════════════
# VOICE / TTS UTIL
# ══════════════════════════════════════════════════════════════════════

def _speak_text(text: str, lang: str = "en", slow: bool = False) -> bytes:
    """
    Convert text to speech using Sarvam AI API with gTTS fallback.
    Automatically translates text to selected language using IndicTrans2 before TTS.
    Supports 16 languages including 10 Indian languages.
    """
    if not text or not text.strip():
        return b""
    
    # Truncate text if too long (Sarvam API limit)
    original_text = text
    if len(text) > 1000:
        text = text[:1000]
    
    # Translate to selected language first
    if lang and lang != "en":
        translated_text = translate_to_language(text, lang)
        if translated_text and translated_text != text:
            text = translated_text
    
    try:
        # Get API key from environment
        api_key = os.environ.get("SARVAM_API_KEY")
        
        if api_key:
            # Try Sarvam API first
            sarvam_lang_map = {
                "en": "en-US",
                "hi": "hi-IN",
                "ta": "ta-IN",
                "te": "te-IN",
                "kn": "kn-IN",
                "ml": "ml-IN",
                "mr": "mr-IN",
                "gu": "gu-IN",
                "bn": "bn-IN",
                "pa": "pa-IN",
                "ur": "ur-IN",
                "es": "es-ES",
                "fr": "fr-FR",
                "de": "de-DE",
                "zh-CN": "zh-CN",
                "ja": "ja-JP",
            }
            
            sarvam_lang = sarvam_lang_map.get(lang, "en-US")
            
            url = "https://api.sarvam.ai/text-to-speech"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": [text],
                "target_language_code": sarvam_lang,
                "speaker": "meera",
                "pitch": 1.0,
                "pace": 1.0,
                "loudness": 1.5
            }
            
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    # Check different possible response structures
                    if "audios" in result and result["audios"]:
                        audio_data = result["audios"][0]
                        if isinstance(audio_data, str):
                            # Base64 encoded audio
                            try:
                                audio_bytes = base64.b64decode(audio_data)
                                return audio_bytes
                            except:
                                pass
                        elif isinstance(audio_data, bytes):
                            return audio_data
                    
                    # Try alternative response structure
                    if "audio" in result:
                        audio_data = result["audio"]
                        if isinstance(audio_data, str):
                            try:
                                audio_bytes = base64.b64decode(audio_data)
                                return audio_bytes
                            except:
                                pass
                        elif isinstance(audio_data, bytes):
                            return audio_data
            except requests.exceptions.RequestException:
                pass  # Fall back to gTTS
        
        # Fallback to gTTS if Sarvam fails or key not set
        try:
            from gtts import gTTS
            
            # Validate language code
            if not lang:
                lang = "en"
            
            tts = gTTS(text=text, lang=lang, slow=slow)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.read()
        except Exception as e:
            return b""
            
    except Exception as e:
        return b""


def _short_from_text(full_text: str, max_sentences: int = 2, fallback_chars: int = 150) -> str:
    """
    Build a short voice-friendly summary from a longer text.
    Always returns a brief snippet (1–2 sentences) at most.
    """
    if not full_text:
        return ""

    sentences = [s.strip() for s in full_text.split(".") if s.strip()]
    if sentences:
        snippet = ". ".join(sentences[:max_sentences]) + "."
        return snippet

    snippet = full_text[:fallback_chars].strip()
    if not snippet.endswith("."):
        snippet += "."
    return snippet


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Brand
    st.markdown("""
    <div class="brand-block">
        <div class="brand-icon">🏥</div>
        <div class="brand-name">MediAssist</div>
        <div class="brand-tagline">Report Intelligence System</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)

    nav_items = [
        ("Dashboard",     "📊"),
        ("Upload Report", "📁"),
        ("Explanation",   "💡"),
        ("Doctor Mode",   "🩺"),
        ("Settings",      "⚙️"),
    ]

    for page_name, icon in nav_items:
        is_active = st.session_state.page == page_name
        btn_type  = "primary" if is_active else "secondary"
        if st.button(f"{icon}  {page_name}", key=f"nav_{page_name}",
                     use_container_width=True, type=btn_type):
            st.session_state.page = page_name
            st.rerun()

    # Patient info
    st.markdown('<div class="nav-label" style="margin-top:20px;">Patient</div>',
                unsafe_allow_html=True)
    st.session_state.patient_age = st.number_input(
        "Age", min_value=1, max_value=120,
        value=st.session_state.patient_age,
        label_visibility="visible",
    )
    st.session_state.patient_gender = st.selectbox(
        "Gender",
        ["Not specified", "Male", "Female", "Other"],
        index=["Not specified", "Male", "Female", "Other"].index(
            st.session_state.patient_gender
        ),
    )

    st.markdown("---")

    # Doctor mode toggle
    st.session_state.doctor_mode = st.toggle(
        "🩺 Doctor Mode",
        value=st.session_state.doctor_mode,
        help="Reveals raw extracted text, JSON data, and diagnostic detail.",
    )

    # Voice & Language Settings
    st.markdown('<div class="nav-label" style="margin-top:20px;">🔊 Voice & Language (Sarvam AI)</div>',
                unsafe_allow_html=True)
    st.session_state.voice_language = st.selectbox(
        "Select Language",
        list(LANGUAGE_CODES.keys()),
        index=list(LANGUAGE_CODES.keys()).index(st.session_state.voice_language) 
            if st.session_state.voice_language in LANGUAGE_CODES else 0,
        help="Choose language for text-to-speech (10 Indian languages supported)",
        key="language_selector"
    )
    
    # Sarvam API Key Setup
    api_key_status = "✅ Configured" if os.environ.get("SARVAM_API_KEY") else "❌ Not Set"
    
    # Language verification display
    lang_code = LANGUAGE_CODES.get(st.session_state.voice_language, "en")
    st.info(f"""
    **Language Selected:** {st.session_state.voice_language} (Code: {lang_code})
    **API Status:** {api_key_status}
    
    🇮🇳 **Indian Languages Supported:**
    - Hindi, Tamil, Telugu, Kannada, Malayalam
    - Marathi, Gujarati, Bengali, Punjabi, Urdu
    
    🔑 **To use Sarvam AI:**
    ```
    $env:SARVAM_API_KEY = "your_sarvam_api_key"
    ```
    Get free API key: sarvam.ai
    """)

    st.markdown("---")
    if st.session_state.stage > 0:
        stage = st.session_state.stage
        steps = [
            ("Upload",      1),
            ("OCR",         1),
            ("Clean",       2),
            ("Extract",     3),
            ("Detect",      4),
            ("Risk Score",  5),
            ("Explain",     6),
            ("Complete",    7),
        ]
        st.markdown("""
        <div class="pipeline-container">
            <div class="pipeline-title">Pipeline Status</div>
        """, unsafe_allow_html=True)

        for i, (label, threshold) in enumerate(steps):
            if stage > threshold:
                dot_cls, lbl_cls = "done", "done"
            elif stage == threshold:
                dot_cls, lbl_cls = "active", "active"
            else:
                dot_cls, lbl_cls = "idle", ""

            st.markdown(f"""
            <div class="pipeline-step">
                <div class="pipeline-dot {dot_cls}"></div>
                <div class="pipeline-step-label {lbl_cls}">{label}</div>
            </div>
            {"<div class='pipeline-connector'></div>" if i < len(steps)-1 else ""}
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="padding:20px 20px 8px;font-size:11px;color:rgba(255,255,255,0.2);
    line-height:1.6;">
    MediAssist v2.0<br>
    AI-powered · Not a medical device<br>
    Made with Gemini · Always consult a doctor
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# UI COMPONENT HELPERS
# ══════════════════════════════════════════════════════════════════════

def _stage_bar(current: int):
    """Render the horizontal pipeline progress bar."""
    stages = [
        ("📤", "Upload"),
        ("🔍", "OCR"),
        ("🧹", "Clean"),
        ("🔬", "Extract"),
        ("⚠️",  "Detect"),
        ("📊", "Risk"),
        ("💡", "Explain"),
        ("✅", "Done"),
    ]

    items_html = ""
    for i, (icon, label) in enumerate(stages):
        if current > i:
            cls = "done"
        elif current == i:
            cls = "active"
        else:
            cls = ""

        items_html += f"""
        <div class="stage-item">
            <div class="stage-icon {cls}">{icon}</div>
            <div class="stage-label {cls}">{label}</div>
        </div>
        """
        if i < len(stages) - 1:
            conn_cls = "done" if current > i else ""
            items_html += f'<div class="stage-connector {conn_cls}"></div>'

    st.markdown(f'<div class="stage-bar">{items_html}</div>', unsafe_allow_html=True)


def _hero_card():
    """Render top hero summary card."""
    s = st.session_state.summary
    if not s:
        st.markdown("""
        <div class="hero-card">
            <div class="hero-eyebrow">Health Overview</div>
            <div class="hero-heading">No Report Analysed Yet</div>
            <div class="hero-description">
                Upload a medical report to see your personalised health summary, 
                lab results, and AI-powered insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    n_total    = s.get("total", 0)
    n_abnormal = s.get("abnormal_count", 0)
    n_normal   = s.get("normal_count", 0)
    heading    = s.get("heading", "")
    desc       = s.get("description", "")

    pill_a = "danger"   if n_abnormal > 2 else ("warning" if n_abnormal > 0 else "success")
    pill_n = "success"

    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-eyebrow">Health Summary</div>
        <div class="hero-heading">{heading}</div>
        <div class="hero-description">{desc}</div>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-value">{n_total}</div>
                <div class="hero-stat-label">Tests Analysed</div>
            </div>
            <div class="hero-stat {pill_n}">
                <div class="hero-stat-value">{n_normal}</div>
                <div class="hero-stat-label">Normal</div>
            </div>
            <div class="hero-stat {pill_a}">
                <div class="hero-stat-value">{n_abnormal}</div>
                <div class="hero-stat-label">Need Attention</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
    ⚠️ <strong>Disclaimer:</strong> MediAssist is for informational purposes only. 
    It does not constitute medical advice, diagnosis, or treatment. 
    Always consult a qualified healthcare professional before making any health decisions.
    </div>
    """, unsafe_allow_html=True)

    # Voice summary playback (short)
    if st.session_state.summary:
        with st.expander("🔊 Listen to summary", expanded=False):
            full = st.session_state.summary.get("description", "")
            if full:
                col_lang, col_btn = st.columns([2, 1])
                with col_lang:
                    current_lang = st.session_state.voice_language
                    lang_code = LANGUAGE_CODES.get(current_lang, "en")
                    st.caption(f"🗣️ Language: {current_lang} ({lang_code})")
                with col_btn:
                    if st.button("Play Summary Audio", key="play_summary_audio"):
                        short_text = _short_from_text(full, max_sentences=2, fallback_chars=180)
                        current_lang = st.session_state.voice_language
                        lang_code = LANGUAGE_CODES.get(current_lang, "en")
                        audio_bytes = _speak_text(short_text, lang=lang_code)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")


def _lab_table():
    df = st.session_state.df

    if df.empty:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <span class="card-title">Lab Results</span>
                <span class="card-badge">No data</span>
            </div>
            <div style="text-align:center;padding:40px;color:#94a3b8;">
                No lab values extracted yet. Upload a report first.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    n_abnormal = (df["Status"].isin(["High", "Low"])).sum()
    badge_cls  = "danger" if n_abnormal > 2 else ("warning" if n_abnormal > 0 else "success")

    rows_html = ""
    for _, row in df.iterrows():
        status = row.get("Status", "Unknown")

        row_cls = {
            "Normal": "row-normal",
            "High":   "row-high",
            "Low":    "row-low"
        }.get(status, "")

        badge_cls2 = {
            "Normal": "badge-normal",
            "High":   "badge-high",
            "Low":    "badge-low"
        }.get(status, "badge-unknown")

        sev = row.get("Severity", "")
        sev_html = (
            f'<span class="sev-tag">{sev}</span>'
            if sev and sev != "None" else ""
        )

        rows_html += f"""
        <tr class="{row_cls}">
            <td class="test-name-cell">{row['Test']}</td>
            <td class="value-cell">{row['Value']}</td>
            <td class="unit-cell">{row.get('Unit','')}</td>
            <td class="ref-cell">{row.get('Reference Range','—')}</td>
            <td class="status-cell"><span class="badge {badge_cls2}">{status}</span>{sev_html}</td>
        </tr>
        """

       # ── Build the full card HTML ──────────────────────────────────────
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'DM Sans', -apple-system, sans-serif; }}

    .card {{
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.11);
        border-radius: 28px;
        overflow: hidden;
        position: relative;
    }}
    .card-header {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 16px 22px 13px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg,rgba(255,255,255,.04) 0%,transparent 100%);
    }}
    .card-title {{ font-size: 15px; font-weight: 700; color: #f2f4f7; }}
    .card-badge {{
        display: inline-flex; align-items: center; padding: 4px 12px;
        border-radius: 9999px; font-size: 10px; font-weight: 700;
        letter-spacing: 0.06em; text-transform: uppercase;
        background: rgba(10,132,255,0.16); border: 1px solid rgba(10,132,255,.30);
        color: #0A84FF;
    }}
    .card-badge.success {{ background: rgba(48,209,88,0.14); border-color: rgba(48,209,88,.30); color: #30D158; }}
    .card-badge.warning {{ background: rgba(255,159,10,0.14); border-color: rgba(255,159,10,.30); color: #FF9F0A; }}
    .card-badge.danger  {{ background: rgba(255,69,58,0.14);  border-color: rgba(255,69,58,.30);  color: #FF453A; }}

    .lab-table-wrap {{ overflow-x: auto; padding: 2px 4px 8px; }}
    .lab-table {{
        width: 100%; border-collapse: separate; border-spacing: 0 2px;
        font-size: 13px; table-layout: fixed; color: #e2e8f0;
    }}
    .lab-table thead th {{
        padding: 10px 14px 12px; font-size: 10px; font-weight: 700;
        letter-spacing: .10em; text-transform: uppercase; color: #4e6070;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        white-space: nowrap; background: transparent; text-align: left;
    }}
    .lab-table thead th:nth-child(1) {{ width: 32%; }}
    .lab-table thead th:nth-child(2) {{ width: 13%; text-align: right; }}
    .lab-table thead th:nth-child(3) {{ width: 11%; text-align: right; }}
    .lab-table thead th:nth-child(4) {{ width: 22%; }}
    .lab-table thead th:nth-child(5) {{ width: 22%; }}
    .lab-table tbody tr {{ transition: background 0.15s ease; }}
    .lab-table td {{
        padding: 14px 12px; font-size: 14px;
        border-bottom: 1px solid rgba(255,255,255,.05);
        vertical-align: middle; color: #a0aec0;
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }}
    .lab-table tbody tr:last-child td {{ border-bottom: none; }}
    .lab-table tbody tr:hover td {{ background: rgba(255,255,255,.04); }}

    .lab-table td:nth-child(2) {{ text-align: right; padding-right: 20px; }}
    .lab-table td:nth-child(3) {{ text-align: right; padding-right: 16px; }}

    .test-name-cell {{ font-weight: 600; color: #f2f4f7 !important; font-size: 13.5px; }}
    .value-cell {{ font-size: 14px; font-weight: 700; color: #f2f4f7 !important; }}
    .unit-cell  {{ font-size: 12px; color: #4e6070; }}
    .ref-cell   {{ font-size: 12px; color: #a0aec0; font-family: 'JetBrains Mono', monospace; }}
    .status-cell {{ white-space: nowrap; }}

    .row-normal td:first-child {{ border-left: 3px solid #30D158; padding-left: 12px; }}
    .row-high   td:first-child {{ border-left: 3px solid #FF453A; padding-left: 12px; }}
    .row-low    td:first-child {{ border-left: 3px solid #0A84FF; padding-left: 12px; }}

    .badge {{
        display: inline-flex; align-items: center; gap: 5px;
        padding: 4px 12px; border-radius: 9999px;
        font-size: 11px; font-weight: 700; letter-spacing: .04em;
    }}
    .badge-normal {{ background: rgba(48,209,88,0.14);  color: #30D158; border: 1px solid rgba(48,209,88,.35); }}
    .badge-high   {{ background: rgba(255,69,58,0.14);  color: #FF453A; border: 1px solid rgba(255,69,58,.35); }}
    .badge-low    {{ background: rgba(10,132,255,0.16); color: #0A84FF; border: 1px solid rgba(10,132,255,.30); }}
    .badge-unknown{{ background: rgba(255,255,255,.06); color: #4e6070; border: 1px solid rgba(255,255,255,0.06); }}

    .sev-tag {{
        display: inline-block; font-size: 10px; padding: 2px 8px;
        border-radius: 9999px; background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.06); color: #4e6070;
        margin-left: 8px; vertical-align: middle;
    }}

    .table-footer {{
        padding: 11px 22px 14px; font-size: 11px; color: #4e6070;
        border-top: 1px solid rgba(255,255,255,0.06);
        display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
    }}
    .legend-dot {{
        display: inline-block; width: 8px; height: 8px;
        border-radius: 50%; margin-right: 4px;
    }}
    .legend-dot.green {{ background: #30D158; box-shadow: 0 0 6px rgba(48,209,88,0.5); }}
    .legend-dot.red   {{ background: #FF453A; box-shadow: 0 0 6px rgba(255,69,58,0.5); }}
    .legend-dot.blue  {{ background: #0A84FF; box-shadow: 0 0 6px rgba(10,132,255,0.5); }}
    </style>
    </head>
    <body style="background:transparent;">
    <div class="card">
        <div class="card-header">
            <span class="card-title">🔬 Lab Results</span>
            <span class="card-badge {badge_cls}">
                {len(df)} tests &nbsp;·&nbsp; {int(n_abnormal)} flagged
            </span>
        </div>
        <div class="lab-table-wrap">
            <table class="lab-table">
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Value</th>
                        <th>Unit</th>
                        <th>Reference Range</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        <div class="table-footer">
            <span><span class="legend-dot green"></span>Normal</span>
            <span><span class="legend-dot red"></span>High (▲)</span>
            <span><span class="legend-dot blue"></span>Low (▼)</span>
        </div>
    </div>
    </body>
    </html>
    """

    # ── Render via iframe so CSS is never stripped by Streamlit ──────
    row_count   = len(df)
    table_height = max(300, 80 + (row_count * 58))
    st.components.v1.html(full_html, height=table_height, scrolling=False)


def _risk_card():
    """Render risk category scores."""
    risks = st.session_state.risk_scores

    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">Risk Analysis</span>
    """, unsafe_allow_html=True)

    if not risks:
        st.markdown("""
            <span class="card-badge">No data</span>
        </div>
        <div style="text-align:center;padding:40px;color:#94a3b8;">
            Upload a report to see risk indicators.
        </div>
    </div>
    """, unsafe_allow_html=True)
        return

    st.markdown(
        '<span class="card-badge">AI Scored</span></div>',
        unsafe_allow_html=True
    )

    for r in risks:
        score = r["score"]
        level = r["level"]

        st.markdown(f"""
        <div class="risk-row">
            <div class="risk-info">
                <div class="risk-name">{r['icon']} {r['category']}</div>
                <div class="risk-sub">{r['tests_abnormal']}/{r['tests_found']} values abnormal</div>
            </div>
            <div class="risk-track">
                <div class="risk-fill {level}" style="width:{score}%"></div>
            </div>
            <div class="risk-pct {level}">{score}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:11px;color:#94a3b8;margin-top:14px;padding-top:12px;
    border-top:1px solid #f0f3f8;">
    Scores reflect the proportion of abnormal values in each category.
    Not a clinical diagnosis.
    </div>
    </div>
    """, unsafe_allow_html=True)


def _chat_panel():
    """Render the chatbot interaction panel."""
    # Chat header
    st.markdown("""
    <div class="chat-header-bar">
        <div class="chat-avatar-wrap">🤖</div>
        <div>
            <div class="chat-name-label">MediAssist AI</div>
            <div class="chat-status-dot">Online</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Message history
    if not st.session_state.chat_history:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                "Hello, I am **MediAssist**.\n\n"
                "I explain your lab report in simple, clear words.\n"
                "I only use the numbers in your report. I do not give medical diagnoses.\n\n"
                "You can ask things like:\n"
                "- \"Is my sugar level high?\"\n"
                "- \"What does low hemoglobin mean?\""
            )

    for msg in st.session_state.chat_history:
        avatar = "🤖" if msg["role"] in ("assistant", "model") else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Ask about your report…"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.spinner("Analyzing clinical data…"):
            reply = chatbot_response(
                user_query=prompt,
                df=st.session_state.df if not st.session_state.df.empty else None,
                history=st.session_state.chat_history[:-1],
            )

        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # Voice playback: very short summary of the answer
        with st.expander("🔊 Listen to short summary", expanded=False):
            col_lang, col_btn = st.columns([2, 1])
            with col_lang:
                current_lang = st.session_state.voice_language
                lang_code = LANGUAGE_CODES.get(current_lang, "en")
                st.caption(f"🗣️ Language: {current_lang} ({lang_code})")
            with col_btn:
                if st.button("Play Answer Audio", key="play_last_answer"):
                    short_text = _short_from_text(reply, max_sentences=2, fallback_chars=180)
                    if not short_text:
                        short_text = "Here is a short summary of your lab result. Please talk to your doctor."
                    current_lang = st.session_state.voice_language
                    lang_code = LANGUAGE_CODES.get(current_lang, "en")
                    audio_bytes = _speak_text(short_text, lang=lang_code)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")

        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# FULL PIPELINE RUNNER
# ══════════════════════════════════════════════════════════════════════

def run_pipeline(uploaded_file):
    """Execute all pipeline stages on the uploaded file."""

    progress = st.progress(0, text="Starting pipeline…")
    status   = st.empty()

    try:
        # ── Stage 1: OCR ──────────────────────────────────────────────
        st.session_state.stage = 1
        status.info("🔍 **Stage 1/7** — Extracting text via OCR…")
        progress.progress(10, text="Stage 1: OCR extraction")

        uploaded_file.seek(0)
        raw_text, ocr_method = extract_text(uploaded_file)
        st.session_state.raw_text   = raw_text
        st.session_state.ocr_method = ocr_method

        if not raw_text or len(raw_text.strip()) < 10:
            status.error(
                "⚠️ Could not extract text from this file. "
                "Ensure the document is clear and readable."
            )
            progress.empty()
            return False

        # ── Stage 2: Clean ────────────────────────────────────────────
        st.session_state.stage = 2
        status.info("🧹 **Stage 2/7** — Cleaning extracted text…")
        progress.progress(25, text="Stage 2: Text cleaning")

        cleaned = clean_text(raw_text)
        st.session_state.cleaned_text = cleaned

        # ── Stage 3: Structured Extraction ───────────────────────────
        st.session_state.stage = 3
        status.info("🔬 **Stage 3/7** — Extracting structured lab parameters…")
        progress.progress(40, text="Stage 3: Structured extraction")

        df = extract_parameters(cleaned)

        # ── Stage 4: Abnormal Detection ───────────────────────────────
        st.session_state.stage = 4
        status.info("⚠️ **Stage 4/7** — Detecting abnormal values…")
        progress.progress(55, text="Stage 4: Abnormal detection")

        if not df.empty:
            df = detect_abnormal(df)
        st.session_state.df = df

        # ── Stage 5: Risk Scoring ─────────────────────────────────────
        st.session_state.stage = 5
        status.info("📊 **Stage 5/7** — Computing risk scores…")
        progress.progress(70, text="Stage 5: Risk scoring")

        risk_scores = compute_risk_scores(df)
        st.session_state.risk_scores = risk_scores

        # ── Stage 6: Explanation Generator ───────────────────────────
        st.session_state.stage = 6
        status.info("💡 **Stage 6/7** — Generating personalised explanation…")
        progress.progress(85, text="Stage 6: Generating explanation")

        summary = generate_summary(
            df,
            age=st.session_state.patient_age,
            gender=st.session_state.patient_gender,
        )
        st.session_state.summary = summary

        # ── Stage 7: Complete ─────────────────────────────────────────
        st.session_state.stage = 7
        progress.progress(100, text="Complete!")
        status.success("✅ **All stages complete.** Report fully analysed.")
        st.session_state.report_ready = True
        return True

    except Exception as e:
        status.error(f"❌ Pipeline error: {e}")
        progress.empty()
        return False

    finally:
        import time; time.sleep(0.5)
        progress.empty()
        status.empty()


# ══════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Overview</div>
        <div class="page-title">Health Dashboard</div>
        <div class="page-subtitle">Your complete medical report at a glance</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.stage > 0:
        _stage_bar(st.session_state.stage)

    _hero_card()

    # --- DOCTOR VERIFICATION BANNER ---
    if st.session_state.doctor_verified:
        st.markdown("""
        <div style="background: rgba(34,197,94,0.1); border: 1px solid #22c55e; padding: 16px; border-radius: 12px; margin-bottom: 20px;">
            <h4 style="color: #4ade80; margin-top: 0; margin-bottom: 12px;">✅ Verified by Attending Doctor</h4>
        """, unsafe_allow_html=True)
        
        # Show doctor information
        if st.session_state.doctor_name or st.session_state.doctor_hospital:
            doctor_info = []
            if st.session_state.doctor_name:
                doctor_info.append(f"**👨‍⚕️ {st.session_state.doctor_name}**")
            if st.session_state.doctor_license:
                doctor_info.append(f"License: {st.session_state.doctor_license}")
            if st.session_state.doctor_hospital:
                doctor_info.append(f"Hospital: {st.session_state.doctor_hospital}")
            if st.session_state.verification_timestamp:
                doctor_info.append(f"Verified on: {st.session_state.verification_timestamp}")
            st.markdown(" | ".join(doctor_info))
        
        # Show digital signature if present
        if st.session_state.digital_signature:
            st.markdown(f"*Digital Signature: {st.session_state.digital_signature}*")
        
        if st.session_state.doctor_notes:
            st.markdown(f"**Clinical Notes:**\n\n{st.session_state.doctor_notes}")
            
        if st.session_state.prescriptions:
            st.markdown("**Prescribed Therapeutics:**")
            for med in st.session_state.prescriptions:
                timestamp = med.get("timestamp", "")
                timestamp_str = f"({timestamp})" if timestamp else ""
                st.markdown(f"- 💊 **{med['name']}** : *{med['dosage']}* {timestamp_str}")
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        _lab_table()
    with col2:
        _risk_card()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card-title" style="margin-bottom:14px;">
        💬 Chat with MediAssist
    </div>
    """, unsafe_allow_html=True)

    _chat_panel()


# ══════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD REPORT
# ══════════════════════════════════════════════════════════════════════

def page_upload():
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Stage 1 — Input</div>
        <div class="page-title">Upload Medical Report</div>
        <div class="page-subtitle">
            Supports PDF (text or scanned), JPG, and PNG formats up to 20 MB
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload hint UI
    st.markdown("""
    <div class="upload-hint">
        <div class="upload-hint-icon">📄</div>
        <div class="upload-hint-title">Drop your report here or click to browse</div>
        <div class="upload-hint-sub">PDF · JPG · PNG · Max 20 MB</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload medical report",
        type=["pdf", "jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="info-pill">
                📎 {uploaded_file.name} &nbsp;·&nbsp; 
                {uploaded_file.size // 1024} KB
            </div>
            """, unsafe_allow_html=True)
        with col2:
            analyse_btn = st.button("🚀 Analyse Report", type="primary",
                                    use_container_width=True)

        if analyse_btn:
            with st.container():
                success = run_pipeline(uploaded_file)

            if success:
                n = len(st.session_state.df)
                ab = st.session_state.summary.get("abnormal_count", 0)

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Tests Found", n)
                with col_b:
                    st.metric("Abnormal", ab, delta=f"-{ab}" if ab else None,
                              delta_color="inverse")
                with col_c:
                    st.metric("OCR Method", st.session_state.ocr_method[:20])

                st.info("✅ Analysis complete. Go to **Dashboard** to view results.")

                # Quick preview
                if not st.session_state.df.empty:
                    with st.expander("📋 Preview extracted lab values"):
                        st.dataframe(st.session_state.df[["Test","Value","Unit",
                                                           "Reference Range","Status","Severity"]],
                                     use_container_width=True)

                # Raw text preview
                if st.session_state.raw_text:
                    with st.expander(f"📄 Raw extracted text ({st.session_state.ocr_method})"):
                        st.text_area(
                            "Extracted text",
                            st.session_state.raw_text[:3000] +
                            ("…" if len(st.session_state.raw_text) > 3000 else ""),
                            height=260,
                            label_visibility="collapsed",
                        )

    # OCR dependency status
    with st.expander("🔧 System / OCR Status"):
        deps = get_dependency_status()
        cols = st.columns(len(deps))
        for col, (lib, ok) in zip(cols, deps.items()):
            with col:
                st.metric(lib, "✅" if ok else "❌")


# ══════════════════════════════════════════════════════════════════════
# PAGE: EXPLANATION
# ══════════════════════════════════════════════════════════════════════

def page_explanation():
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Stage 6 — Insights</div>
        <div class="page-title">Personalised Explanation</div>
        <div class="page-subtitle">Plain-language breakdown of your findings and lifestyle guidance</div>
    </div>
    """, unsafe_allow_html=True)

    s = st.session_state.summary
    if not s:
        st.info("👆 Please upload a report first.")
        return

    findings = s.get("findings", [])
    lifestyle = s.get("lifestyle", [])

    # ── Findings ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">Key Findings</span>
        </div>
    """, unsafe_allow_html=True)

    if not findings:
        st.markdown("""
        <div style="text-align:center;padding:30px;color:#94a3b8;">
            ✅ No abnormal values detected. All results are within normal ranges.
        </div>
        """, unsafe_allow_html=True)
    else:
        for f in findings:
            status = f["status"]
            icon_cls = {"High": "high", "Low": "low"}.get(status, "normal")
            icon     = {"High": "⬆️", "Low": "⬇️"}.get(status, "✅")

            explanation_html = (
                f'<div style="font-size:13px;color:#4b6080;margin-top:5px;'
                f'line-height:1.6;">{f["explanation"]}</div>'
                if f.get("explanation") else ""
            )

            st.markdown(f"""
            <div class="finding-item">
                <div class="finding-icon {icon_cls}">{icon}</div>
                <div class="finding-text">
                    <div class="finding-name">
                        {f['name']}
                        <span style="font-size:12px;font-weight:400;color:#94a3b8;margin-left:8px;">
                            {f['value']} {f['unit']} · Ref: {f['ref_range']}
                        </span>
                    </div>
                    <div class="finding-desc">
                        Your value is {f['severity']} {f['direction']} than the normal range.
                    </div>
                    {explanation_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Voice: short explanation snippet
    explanation_voice_text_parts = []
    if findings:
        for f in findings:
            explanation_voice_text_parts.append(
                f"{f['name']} : your value is {f['severity']} {f['direction']} than the normal range."
            )
    explanation_voice_text = " ".join(explanation_voice_text_parts).strip()

    if explanation_voice_text:
        with st.expander("🔊 Listen to explanation", expanded=False):
            col_lang, col_btn = st.columns([2, 1])
            with col_lang:
                current_lang = st.session_state.voice_language
                lang_code = LANGUAGE_CODES.get(current_lang, "en")
                st.caption(f"🗣️ Language: {current_lang} ({lang_code})")
            with col_btn:
                if st.button("Play Explanation Audio", key="play_explanation_audio"):
                    short_text = _short_from_text(explanation_voice_text, max_sentences=2, fallback_chars=180)
                    current_lang = st.session_state.voice_language
                    lang_code = LANGUAGE_CODES.get(current_lang, "en")
                    audio_bytes = _speak_text(short_text, lang=lang_code)
                    if audio_bytes:
                        st.audio(audio_bytes, format="audio/mp3")

    # ── Lifestyle Suggestions ─────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">Lifestyle Suggestions</span>
            <span class="card-badge">Personalised</span>
        </div>
    """, unsafe_allow_html=True)

    for tip in lifestyle:
        st.markdown(
            f'<div style="padding:8px 0;font-size:13px;color:#1e3a5f;'
            f'border-bottom:1px solid #f8fafc;">{tip}</div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div style="font-size:12px;color:#94a3b8;margin-top:14px;padding-top:10px;
    border-top:1px solid #f0f3f8;">
    💡 These are general wellness suggestions, not personalised medical advice.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    ⚠️ <strong>Important:</strong> This explanation is AI-generated for informational purposes only.
    It does not constitute a medical opinion. Please consult your doctor to discuss
    your results and any recommended follow-up.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: DOCTOR MODE (STAGE 7)
# ══════════════════════════════════════════════════════════════════════

def page_doctor_mode():
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Stage 7 — Verification</div>
        <div class="page-title">Doctor Mode</div>
        <div class="page-subtitle">Raw data, structured JSON, diagnostic detail, and therapeutics</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.doctor_mode:
        st.warning("🔒 Toggle **Doctor Mode** in the sidebar to access this view.")
        return

    if not st.session_state.report_ready:
        st.info("No report analysed yet. Go to **Upload Report** first.")
        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Raw Text", "🔬 Structured Data",
                                       "📦 JSON Export", "📊 Risk Detail", "✍️ Clinical Actions"])

    with tab1:
        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <span class="card-title">Extracted Raw Text</span>
                <span class="card-badge">{st.session_state.ocr_method}</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="doctor-panel">{st.session_state.raw_text}</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download Raw Text",
                               data=st.session_state.raw_text,
                               file_name="raw_extracted.txt",
                               mime="text/plain")
        with col2:
            st.download_button("⬇️ Download Cleaned Text",
                               data=st.session_state.cleaned_text,
                               file_name="cleaned_text.txt",
                               mime="text/plain")

        # Voice read-aloud of a short excerpt of raw text
        preview_voice = st.session_state.raw_text[:800]
        if preview_voice:
            with st.expander("🔊 Listen to raw text excerpt", expanded=False):
                col_lang, col_btn = st.columns([2, 1])
                with col_lang:
                    current_lang = st.session_state.voice_language
                    lang_code = LANGUAGE_CODES.get(current_lang, "en")
                    st.caption(f"🗣️ Language: {current_lang} ({lang_code})")
                with col_btn:
                    if st.button("Play Raw Text Audio", key="play_raw_audio"):
                        short_text = _short_from_text(preview_voice, max_sentences=2, fallback_chars=180)
                        current_lang = st.session_state.voice_language
                        lang_code = LANGUAGE_CODES.get(current_lang, "en")
                        audio_bytes = _speak_text(short_text, lang=lang_code)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <span class="card-title">Structured Lab Data</span>
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df, use_container_width=True)
        else:
            st.info("No structured data available.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Lab Results JSON**")
            if not st.session_state.df.empty:
                json_str = st.session_state.df.to_json(orient="records", indent=2)
                st.code(json_str, language="json")
                st.download_button("⬇️ Download JSON", data=json_str,
                                   file_name="lab_results.json",
                                   mime="application/json")
                st.download_button("⬇️ Download CSV",
                                   data=st.session_state.df.to_csv(index=False),
                                   file_name="lab_results.csv",
                                   mime="text/csv")

        with col_b:
            st.markdown("**AI Summary JSON**")
            st.json(st.session_state.summary)

    with tab4:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <span class="card-title">Risk Score Detail</span>
            </div>
        """, unsafe_allow_html=True)
        if st.session_state.risk_scores:
            risk_df = pd.DataFrame(st.session_state.risk_scores)
            st.dataframe(risk_df, use_container_width=True)
            st.markdown("**Risk Insights**")
            for r in st.session_state.risk_scores:
                st.info(f"{r['icon']} **{r['category']}**: {r['insight']}")
        else:
            st.info("No risk data available.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <span class="card-title">Physician Verification & Therapeutics</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Doctor Authentication Section
        st.markdown("### 👨‍⚕️ Doctor Information")
        col_doc1, col_doc2, col_doc3 = st.columns(3)
        with col_doc1:
            st.session_state.doctor_name = st.text_input(
                "Doctor's Name", 
                value=st.session_state.doctor_name,
                placeholder="Dr. John Smith"
            )
        with col_doc2:
            st.session_state.doctor_license = st.text_input(
                "License/Registration No.", 
                value=st.session_state.doctor_license,
                placeholder="MD-12345"
            )
        with col_doc3:
            st.session_state.doctor_hospital = st.text_input(
                "Hospital/Clinic", 
                value=st.session_state.doctor_hospital,
                placeholder="City Hospital"
            )
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Enhanced Doctor Features - Row 1: Urgency & Follow-up
        st.markdown("### ⚡ Clinical Assessment")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.session_state.urgency_level = st.selectbox(
                "Urgency Level",
                ["Normal", "Moderate", "High", "Critical"],
                index=["Normal", "Moderate", "High", "Critical"].index(st.session_state.urgency_level)
            )
        with col_u2:
            st.session_state.follow_up_date = st.date_input(
                "Follow-up Date",
                value=st.session_state.follow_up_date
            )
        
        # Patient Allergies
        st.session_state.patient_allergies = st.text_input(
            "🚫 Patient Allergies",
            value=st.session_state.patient_allergies,
            placeholder="e.g., Penicillin, Aspirin, Shellfish"
        )
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Lab Interpretations
        st.markdown("### 🔬 Detailed Lab Interpretations")
        st.session_state.lab_interpretations = st.text_area(
            "Lab Result Analysis",
            value=st.session_state.lab_interpretations,
            height=100,
            placeholder="Detailed interpretation of lab findings, trends, and clinical significance..."
        )
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Verification Toggle
        st.markdown("### ✅ Clinical Verification")
        verification_toggled = st.toggle(
            "Mark Report as Clinically Verified", 
            value=st.session_state.doctor_verified
        )
        
        if verification_toggled and not st.session_state.doctor_verified:
            st.session_state.verification_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.session_state.doctor_verified = verification_toggled
        
        if st.session_state.doctor_verified and st.session_state.verification_timestamp:
            st.markdown(f"""
            <div style="background: rgba(34,197,94,0.1); border: 1px solid #22c55e; 
                        padding: 10px; border-radius: 8px; margin: 10px 0;">
                <small>✅ Verified on: {st.session_state.verification_timestamp}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Digital Signature Section
        st.markdown("### ✍️ Digital Signature")
        st.session_state.digital_signature = st.text_input(
            "Digital Signature", 
            value=st.session_state.digital_signature,
            placeholder="Dr. John Smith, MD - Cardiologist"
        )
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Diagnosis Notes
        st.markdown("### 🩺 Diagnosis & Clinical Notes")
        st.session_state.diagnosis_notes = st.text_area(
            "Diagnosis & Observations", 
            value=st.session_state.diagnosis_notes, 
            height=100,
            placeholder="Primary diagnosis, differential diagnoses, clinical observations..."
        )
        
        # Clinical Notes
        st.markdown("### 📝 Physician's Notes")
        st.session_state.doctor_notes = st.text_area(
            "Additional Clinical Notes", 
            value=st.session_state.doctor_notes, 
            height=80,
            placeholder="Follow-up recommendations, patient education, lifestyle modifications..."
        )
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Contraindications
        st.markdown("### ⚠️ Contraindications & Warnings")
        st.session_state.contraindications = st.text_area(
            "Drug Interactions & Contraindications",
            value=st.session_state.contraindications,
            height=80,
            placeholder="Known contraindications, drug interactions, medical conditions to avoid..."
        )
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Test Recommendations
        st.markdown("### 🧪 Recommended Tests")
        col_tr1, col_tr2 = st.columns([3, 1])
        with col_tr1:
            new_test = st.text_input(
                "Add Test Recommendation",
                placeholder="e.g., Follow-up Blood Glucose in 3 months",
                key="test_rec_input"
            )
        with col_tr2:
            if st.button("➕ Add Test", key="add_test"):
                if new_test:
                    if new_test not in st.session_state.test_recommendations:
                        st.session_state.test_recommendations.append(new_test)
                        st.rerun()
        
        if st.session_state.test_recommendations:
            st.markdown("**Recommended Tests:**")
            for i, test in enumerate(st.session_state.test_recommendations):
                col_t1, col_t2 = st.columns([4, 1])
                with col_t1:
                    st.markdown(f"- 🧪 {test}")
                with col_t2:
                    if st.button("❌", key=f"remove_test_{i}"):
                        st.session_state.test_recommendations.pop(i)
                        st.rerun()
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Referral Specialists
        st.markdown("### 👥 Specialist Referrals")
        col_ref1, col_ref2 = st.columns([3, 1])
        with col_ref1:
            new_specialist = st.text_input(
                "Add Specialist Referral",
                placeholder="e.g., Cardiologist for cardiac evaluation",
                key="referral_input"
            )
        with col_ref2:
            if st.button("➕ Add Referral", key="add_referral"):
                if new_specialist:
                    if new_specialist not in st.session_state.referral_specialists:
                        st.session_state.referral_specialists.append(new_specialist)
                        st.rerun()
        
        if st.session_state.referral_specialists:
            st.markdown("**Specialist Referrals:**")
            for i, spec in enumerate(st.session_state.referral_specialists):
                col_s1, col_s2 = st.columns([4, 1])
                with col_s1:
                    st.markdown(f"- 👨‍⚕️ {spec}")
                with col_s2:
                    if st.button("❌", key=f"remove_spec_{i}"):
                        st.session_state.referral_specialists.pop(i)
                        st.rerun()
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        st.markdown("### 💊 Prescriptions")
        
        col_m1, col_m2 = st.columns([2, 2])
        with col_m1:
            med_name = st.text_input("Medication Name (e.g., Metformin)", key="med_name_input")
        with col_m2:
            med_dosage = st.text_input("Dosage & Frequency (e.g., 500mg BD)", key="med_dosage_input")
            
        if st.button("➕ Add Medication"):
            if med_name and med_dosage:
                st.session_state.prescriptions.append({
                    "name": med_name, 
                    "dosage": med_dosage,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.rerun()
                
        if st.session_state.prescriptions:
            st.markdown("<br>**Current Prescriptions List:**", unsafe_allow_html=True)
            for i, med in enumerate(st.session_state.prescriptions):
                timestamp = med.get("timestamp", "")
                timestamp_str = f"<small>🕐 {timestamp}</small>" if timestamp else ""
                col_p1, col_p2 = st.columns([4, 1])
                with col_p1:
                    st.markdown(f"- 💊 **{med['name']}** : *{med['dosage']}* {timestamp_str}")
                with col_p2:
                    if st.button("🗑️", key=f"remove_med_{i}"):
                        st.session_state.prescriptions.pop(i)
                        st.rerun()
            
            if st.button("🗑️ Clear All Prescriptions"):
                st.session_state.prescriptions = []
                st.rerun()
        
        st.markdown("<hr style='border-color: rgba(30,64,175,0.7);'>", unsafe_allow_html=True)
        
        # Export doctor's report
        st.markdown("### 📄 Export Report")
        doctor_report = f"""
MEDIASSIST - DOCTOR'S CLINICAL REPORT
=====================================

PATIENT INFORMATION:
- Age: {st.session_state.patient_age}
- Gender: {st.session_state.patient_gender}
- Allergies: {st.session_state.patient_allergies or 'None reported'}

PHYSICIAN DETAILS:
- Doctor: {st.session_state.doctor_name}
- License: {st.session_state.doctor_license}
- Hospital: {st.session_state.doctor_hospital}
- Verified: {'Yes' if st.session_state.doctor_verified else 'No'}
- Verification Date: {st.session_state.verification_timestamp or 'N/A'}

CLINICAL ASSESSMENT:
- Urgency Level: {st.session_state.urgency_level}
- Follow-up Date: {st.session_state.follow_up_date}

DIAGNOSIS:
{st.session_state.diagnosis_notes or 'N/A'}

LAB INTERPRETATIONS:
{st.session_state.lab_interpretations or 'N/A'}

CONTRAINDICATIONS & WARNINGS:
{st.session_state.contraindications or 'None documented'}

PHYSICIAN NOTES:
{st.session_state.doctor_notes or 'N/A'}

PRESCRIPTIONS:
"""
        if st.session_state.prescriptions:
            for med in st.session_state.prescriptions:
                doctor_report += f"\n- {med['name']}: {med['dosage']} (Added: {med.get('timestamp', 'N/A')})"
        else:
            doctor_report += "\nNone prescribed"
        
        doctor_report += "\n\nRECOMMENDED TESTS:\n"
        if st.session_state.test_recommendations:
            for test in st.session_state.test_recommendations:
                doctor_report += f"\n- {test}"
        else:
            doctor_report += "\nNone"
        
        doctor_report += "\n\nSPECIALIST REFERRALS:\n"
        if st.session_state.referral_specialists:
            for spec in st.session_state.referral_specialists:
                doctor_report += f"\n- {spec}"
        else:
            doctor_report += "\nNone"
        
        doctor_report += f"\n\nDIGITAL SIGNATURE:\n{st.session_state.digital_signature or 'Not signed'}\n"
        doctor_report += f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                "📄 Download Doctor's Report (TXT)",
                data=doctor_report,
                file_name=f"doctor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        with col_exp2:
            st.download_button(
                "📋 Download Report Data (JSON)",
                data=json.dumps({
                    "doctor": st.session_state.doctor_name,
                    "verified": st.session_state.doctor_verified,
                    "urgency": st.session_state.urgency_level,
                    "diagnosis": st.session_state.diagnosis_notes,
                    "lab_interpretations": st.session_state.lab_interpretations,
                    "prescriptions": st.session_state.prescriptions,
                    "test_recommendations": st.session_state.test_recommendations,
                    "referrals": st.session_state.referral_specialists,
                    "follow_up_date": str(st.session_state.follow_up_date),
                }, indent=2),
                file_name=f"doctor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════

def page_settings():
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Configuration</div>
        <div class="page-title">Settings</div>
        <div class="page-subtitle">Customise MediAssist to your preferences</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Patient Profile ───────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">Patient Profile</span>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120, value=st.session_state.patient_age)
        st.session_state.patient_age = age
    with col2:
        gender = st.selectbox("Gender",
                              ["Not specified", "Male", "Female", "Other"],
                              index=["Not specified","Male","Female","Other"].index(
                                  st.session_state.patient_gender))
        st.session_state.patient_gender = gender

    st.info("💡 Age ≥ 60 activates senior-friendly explanation language.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── AI Settings ───────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">AI Assistant (Gemini API)</span>
        </div>
    """, unsafe_allow_html=True)

    if os.environ.get("GEMINI_API_KEY"):
        st.success("✅ Gemini API key loaded from environment. Full AI responses are active.")
    else:
        st.warning("⚠️ Gemini API key not found. Set the GEMINI_API_KEY environment variable for full AI chat.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── OCR Status ────────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">OCR Dependencies</span>
        </div>
    """, unsafe_allow_html=True)

    deps = get_dependency_status()
    cols = st.columns(len(deps))
    for col, (lib, ok) in zip(cols, deps.items()):
        with col:
            st.metric(lib, "✅ Ready" if ok else "❌ Missing")

    st.markdown("""
    <div style="font-size:12px;color:#94a3b8;margin-top:8px;">
    Install missing libraries: 
    <code>pip install pdfplumber pdf2image Pillow opencv-python-headless pytesseract</code><br>
    Also install: <code>sudo apt-get install tesseract-ocr poppler-utils</code>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Data Management ───────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-title">Session Data</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear All Session Data", type="secondary"):
        for key in ["raw_text", "ocr_method", "cleaned_text", "summary",
                    "risk_scores", "chat_history", "report_ready",
                    "doctor_notes", "doctor_verified", "api_key",
                    "doctor_name", "doctor_license", "doctor_hospital",
                    "verification_timestamp", "digital_signature"]:
            if key in ["risk_scores", "chat_history", "prescriptions"]:
                st.session_state[key] = []
            elif key == "summary":
                st.session_state[key] = {}
            elif key in ["report_ready", "doctor_verified"]:
                st.session_state[key] = False
            else:
                st.session_state[key] = ""

        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

        st.session_state.df    = pd.DataFrame()
        st.session_state.stage = 0
        st.success("Session cleared successfully.")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════

page = st.session_state.page

if page == "Dashboard":
    page_dashboard()
elif page == "Upload Report":
    page_upload()
elif page == "Explanation":
    page_explanation()
elif page == "Doctor Mode":
    page_doctor_mode()
elif page == "Settings":
    page_settings() 
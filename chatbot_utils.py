"""
chatbot_utils.py
Stage 8 — Chatbot Interaction Layer
─────────────────────────────────────
Powered by Gemini API with Adaptive Complexity & Multi-Language Support.
"""

import os
import pandas as pd
from typing import Optional, List

# ══════════════════════════════════════════════════════════════════════
# ADAPTIVE SYSTEM PROMPT
# ══════════════════════════════════════════════════════════════════════

_SYSTEM_PROMPT = """You are MediAssist, an advanced clinical AI assistant.
Your job is to help patients understand their lab results. 

ADAPTIVE COMPLEXITY INSTRUCTIONS (CRITICAL):
1. ANALYZE THE USER'S PROMPT COMPLEXITY:
   - **Simple/Short Prompts** (e.g., "Is this bad?", "What does this mean?", "Summary"):
     -> Respond in **SIMPLE, PLAIN LANGUAGE**. Use short sentences. Avoid medical jargon. Be reassuring and direct.
   - **Detailed/Technical Prompts** (e.g., "Explain the pathophysiology of high TSH", "Relationship between creatinine and eGFR"):
     -> Respond in **DETAILED, CLINICAL DEPTH**. Use appropriate medical terminology. Explain mechanisms. Provide comprehensive context.

COMPARISON & HISTORY RULES:
1. If 'PATIENT HISTORY' is provided in the context, compare current results with previous values.
2. Highlight significant changes (e.g., "Your cholesterol has improved from 240 to 200").
3. If a value was abnormal before and is now normal, explicitly celebrate this improvement.

STRICT SAFETY RULES:
1. ONLY discuss findings present in the structured lab data provided. Do NOT speculate.
2. Provide clinical context for abnormal values based on standard guidelines.
3. Do NOT prescribe or recommend specific medications. You may discuss general therapeutic classes for educational purposes only.
4. Always conclude detailed responses by advising consultation with their attending physician.
"""

def _build_context(df: Optional[pd.DataFrame], patient_history: List[dict] = None) -> str:
    lines = []
    
    # Current Data
    if df is not None and not df.empty:
        lines.append("📊 CURRENT LAB RESULTS (Active Report):")
        for _, row in df.iterrows():
            lines.append(
                f"  • {row['Test']}: {row['Value']} {row.get('Unit','')} "
                f"| Status: {row.get('Status','Unknown')} "
                f"| Severity: {row.get('Severity','—')}"
            )
    else:
        lines.append("No current clinical data available.")

    # Historical Data
    if patient_history:
        lines.append("\n🗄️ PATIENT HISTORY (Previous Visits for Comparison):")
        # Sort newest first and take up to 3 previous visits
        sorted_hist = sorted(patient_history, key=lambda x: x.get('timestamp', ''), reverse=True)[:3]
        for rec in sorted_hist:
            date_str = rec.get('date', 'Unknown Date')
            lines.append(f"\n[Visit Date: {date_str}]")
            for item in rec.get('lab_data', []):
                lines.append(f"  - {item['Test']}: {item['Value']} {item.get('Unit','')}")

    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════════
# CHATBOT RESPONSE ENGINE
# ══════════════════════════════════════════════════════════════════════

def chatbot_response(
    user_query: str,
    df: Optional[pd.DataFrame],
    history: List[dict],
    patient_history: List[dict] = None,
    language: str = "English"  # MULTI-LANGUAGE PARAMETER ADDED HERE
) -> str:
    try:
        import google.generativeai as genai
        
        # Get API key from environment variable
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        
        if not api_key:
            return "ERROR: Gemini API key not configured. Please set the GEMINI_API_KEY environment variable."

        genai.configure(api_key=api_key)
        data_context = _build_context(df, patient_history)
        
        # CONSTRUCT HISTORY WITH MULTILINGUAL & ADAPTIVE INSTRUCTIONS
        lang_instruction = f"IMPORTANT: You MUST respond strictly in {language}."
        full_system_prompt = f"{_SYSTEM_PROMPT}\n\n{lang_instruction}"

        gemini_history = []
        
        # Inject System Prompt 
        instruction_payload = (
            f"SYSTEM INSTRUCTIONS:\n{full_system_prompt}\n\n"
            f"CURRENT DATA:\n{data_context}\n\n"
            f"CRITICAL: Analyze my prompt's complexity. If simple -> use plain language. If detailed -> use clinical depth. ALWAYS reply in {language}."
        )
        
        gemini_history.append({"role": "user", "parts": [instruction_payload]})
        gemini_history.append({"role": "model", "parts": [f"Understood. I will provide adaptive responses in {language} based on the lab data."] })
        
        # Add actual chat history safely mapped to Gemini's role naming
        for turn in history:
            role = "user" if turn.get("role") in ["user", "human"] else "model"
            gemini_history.append({"role": role, "parts": [turn["content"]]})

        # DYNAMIC MODEL SELECTION (Fix for 404 Errors)
        # Query available models to ensure we only use one that exists for this API key.
        try:
            valid_models = [
                m.name for m in genai.list_models() 
                if 'generateContent' in m.supported_generation_methods
            ]
        except Exception:
            valid_models = []

        # Priority: Flash > 1.5 Pro > 1.0 Pro > Generic
        preferences = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro',
            'models/gemini-pro'
        ]
        
        chosen_model = None
        for pref in preferences:
            if pref in valid_models:
                chosen_model = pref
                break
        
        if not chosen_model:
            if valid_models:
                chosen_model = valid_models[0]
            else:
                chosen_model = 'gemini-pro'
        
        model = genai.GenerativeModel(chosen_model)
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(user_query)
        return response.text

    except ImportError:
        return "CRITICAL ERROR: The Gemini library is missing! Run: pip install google-generativeai"
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "AI is currently busy (Rate Limit). Please wait a moment and try again."
        return f"GEMINI API CRASHED! The exact error is: {error_msg}"

# ══════════════════════════════════════════════════════════════════════
# RULE-BASED FALLBACK
# ══════════════════════════════════════════════════════════════════════
def _rule_based(user_query: str, df: Optional[pd.DataFrame]) -> str:
    return "This should not appear."
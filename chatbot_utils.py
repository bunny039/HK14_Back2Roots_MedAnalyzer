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

ADAPTIVE COMPLEXITY RULES:
1. MATCH THE USER'S DEPTH: 
   - If the user asks a simple question (e.g., "How is my sugar?", "Is this bad?"), provide a direct, concise, and reassuring answer in plain language.
   - If the user asks for details, "why", or "pathophysiology" (e.g., "Explain why my WBC is high" or "What are the implications?"), provide a deep-dive response using intermediate medical terminology (e.g., 'leukocytosis', 'renal filtration').

STRICT SAFETY RULES:
1. ONLY discuss findings present in the structured lab data provided. Do NOT speculate.
2. Provide clinical context for abnormal values based on standard guidelines.
3. Do NOT prescribe or recommend specific medications. You may discuss general therapeutic classes for educational purposes only.
4. Always conclude detailed responses by advising consultation with their attending physician.
"""

def _build_context(df: Optional[pd.DataFrame]) -> str:
    if df is None or df.empty:
        return "No clinical data is available."
    lines = ["PATIENT LAB RESULTS (Context):"]
    for _, row in df.iterrows():
        # Passing status and severity helps the AI quickly gauge urgency
        lines.append(
            f"  • {row['Test']}: {row['Value']} {row.get('Unit','')} "
            f"| Status: {row.get('Status','Unknown')} "
            f"| Severity: {row.get('Severity','—')}"
        )
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════════
# CHATBOT RESPONSE ENGINE
# ══════════════════════════════════════════════════════════════════════

def chatbot_response(
    user_query: str,
    df: Optional[pd.DataFrame],
    history: List[dict],
    language: str = "English"  # MULTI-LANGUAGE PARAMETER ADDED HERE
) -> str:
    try:
        import google.generativeai as genai
        
        # Get API key from environment variable
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        
        if not api_key:
            return "ERROR: Gemini API key not configured. Please set the GEMINI_API_KEY environment variable."

        genai.configure(api_key=api_key)
        data_context = _build_context(df)
        
        # BULLETPROOF AUTO-MODEL DETECTION
        valid_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        chosen_model = None
        for pref in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if pref in valid_models:
                chosen_model = pref
                break
                
        if not chosen_model and valid_models:
            chosen_model = valid_models[0]
            
        if not chosen_model:
            return "GEMINI ERROR: Your API key does not have access to any text generation models."

        model = genai.GenerativeModel(model_name=chosen_model)

        # CONSTRUCT HISTORY WITH MULTILINGUAL & ADAPTIVE INSTRUCTIONS
        lang_instruction = f"IMPORTANT: You MUST respond strictly in {language}."
        full_system_prompt = f"{_SYSTEM_PROMPT}\n\n{lang_instruction}"

        gemini_history = []
        
        # Inject System Prompt 
        instruction_payload = (
            f"SYSTEM INSTRUCTIONS:\n{full_system_prompt}\n\n"
            f"CURRENT DATA:\n{data_context}\n\n"
            f"Note: Adjust your depth based on my prompt. ALWAYS reply in {language}."
        )
        
        gemini_history.append({"role": "user", "parts": [instruction_payload]})
        gemini_history.append({"role": "model", "parts": [f"Understood. I will provide adaptive responses in {language} based on the lab data."] })
        
        # Add actual chat history safely mapped to Gemini's role naming
        for turn in history:
            role = "user" if turn.get("role") in ["user", "human"] else "model"
            gemini_history.append({"role": role, "parts": [turn["content"]]})

        # SEND MESSAGE
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
"""
extraction_utils.py
Stages 3, 4, 5, 6: Structured Extraction → Abnormal Detection → Risk Scoring → Explanation
─────────────────────────────────────────────────────────────────────────────────────────────
"""

import re
import numpy as np
import pandas as pd
from typing import Optional, Tuple, List


# ══════════════════════════════════════════════════════════════════════
# STAGE 3 — STRUCTURED EXTRACTION
# ══════════════════════════════════════════════════════════════════════

# ── Reference database ────────────────────────────────────────────────
# Keys: lowercase aliases → (ref_min, ref_max, unit, canonical_name)
REFERENCE_DB = {
    # ── Haematology ───────────────────────────────────────────────────
    "hemoglobin":        (12.0, 17.5, "g/dL",    "Hemoglobin"),
    "haemoglobin":       (12.0, 17.5, "g/dL",    "Hemoglobin"),
    "hb":                (12.0, 17.5, "g/dL",    "Hemoglobin"),
    "hgb":               (12.0, 17.5, "g/dL",    "Hemoglobin"),
    "hematocrit":        (36.0, 52.0, "%",        "Hematocrit"),
    "haematocrit":       (36.0, 52.0, "%",        "Hematocrit"),
    "packed cell volume":(36.0, 52.0, "%",        "Packed Cell Volume"),
    "pcv":               (36.0, 52.0, "%",        "Packed Cell Volume"),
    "rbc":               (4.0,  5.9,  "M/µL",    "Red Blood Cells"),
    "red blood cell":    (4.0,  5.9,  "M/µL",    "Red Blood Cells"),
    "wbc":               (4.0,  11.0, "K/µL",    "White Blood Cells"),
    "white blood cell":  (4.0,  11.0, "K/µL",    "White Blood Cells"),
    "leukocyte":         (4.0,  11.0, "K/µL",    "Leukocytes"),
    "platelet":          (150,  400,  "K/µL",    "Platelets"),
    "thrombocyte":       (150,  400,  "K/µL",    "Platelets"),
    "mcv":               (80,   100,  "fL",       "MCV"),
    "mch":               (27,   33,   "pg",       "MCH"),
    "mchc":              (32,   36,   "g/dL",    "MCHC"),
    "rdw":               (11.5, 14.5, "%",        "RDW"),
    "neutrophil":        (40,   75,   "%",        "Neutrophils"),
    "lymphocyte":        (20,   45,   "%",        "Lymphocytes"),
    "monocyte":          (2,    10,   "%",        "Monocytes"),
    "eosinophil":        (1,    6,    "%",        "Eosinophils"),
    "basophil":          (0,    1,    "%",        "Basophils"),

    # ── Glucose / Diabetes ────────────────────────────────────────────
    "glucose":           (70,  100,   "mg/dL",   "Blood Glucose"),
    "fasting glucose":   (70,  100,   "mg/dL",   "Fasting Blood Glucose"),
    "fasting sugar":     (70,  100,   "mg/dL",   "Fasting Blood Sugar"),
    "fbs":               (70,  100,   "mg/dL",   "Fasting Blood Sugar"),
    "random glucose":    (70,  140,   "mg/dL",   "Random Blood Glucose"),
    "random blood sugar":(70,  140,   "mg/dL",   "Random Blood Sugar"),
    "rbs":               (70,  140,   "mg/dL",   "Random Blood Sugar"),
    "blood sugar":       (70,  140,   "mg/dL",   "Blood Sugar"),
    "hba1c":             (4.0,  5.6,  "%",        "HbA1c"),
    "glycated hemoglobin":(4.0, 5.6,  "%",        "Glycated Hemoglobin"),

    # ── Lipids ────────────────────────────────────────────────────────
    "total cholesterol": (0,   200,   "mg/dL",   "Total Cholesterol"),
    "cholesterol":       (0,   200,   "mg/dL",   "Total Cholesterol"),
    "ldl":               (0,   130,   "mg/dL",   "LDL Cholesterol"),
    "hdl":               (40,  60,    "mg/dL",   "HDL Cholesterol"),
    "triglyceride":      (0,   150,   "mg/dL",   "Triglycerides"),
    "vldl":              (0,   30,    "mg/dL",   "VLDL"),
    "non-hdl":           (0,   160,   "mg/dL",   "Non-HDL Cholesterol"),

    # ── Liver Function ────────────────────────────────────────────────
    "sgpt":              (0,   40,    "U/L",     "SGPT (ALT)"),
    "alt":               (0,   40,    "U/L",     "ALT"),
    "sgot":              (0,   40,    "U/L",     "SGOT (AST)"),
    "ast":               (0,   40,    "U/L",     "AST"),
    "alkaline phosphatase":(44, 147,  "U/L",     "Alkaline Phosphatase"),
    "alp":               (44,  147,   "U/L",     "ALP"),
    "ggt":               (0,   60,    "U/L",     "GGT"),
    "total bilirubin":   (0.2, 1.2,   "mg/dL",   "Bilirubin Total"),
    "bilirubin":         (0.2, 1.2,   "mg/dL",   "Bilirubin Total"),
    "direct bilirubin":  (0,   0.3,   "mg/dL",   "Bilirubin Direct"),
    "indirect bilirubin":(0,   0.9,   "mg/dL",   "Bilirubin Indirect"),
    "albumin":           (3.5, 5.0,   "g/dL",    "Albumin"),
    "total protein":     (6.0, 8.3,   "g/dL",    "Total Protein"),
    "globulin":          (2.0, 3.5,   "g/dL",    "Globulin"),

    # ── Kidney Function ───────────────────────────────────────────────
    "creatinine":        (0.6, 1.2,   "mg/dL",   "Creatinine"),
    "serum creatinine":  (0.6, 1.2,   "mg/dL",   "Serum Creatinine"),
    "blood urea nitrogen":(7,  20,    "mg/dL",   "BUN"),
    "bun":               (7,   20,    "mg/dL",   "BUN"),
    "urea":              (7,   20,    "mg/dL",   "Blood Urea"),
    "uric acid":         (2.4, 7.0,   "mg/dL",   "Uric Acid"),
    "egfr":              (60,  120,   "mL/min",  "eGFR"),

    # ── Thyroid ───────────────────────────────────────────────────────
    "tsh":               (0.4, 4.0,   "mIU/L",   "TSH"),
    "thyroid stimulating":(0.4,4.0,   "mIU/L",   "TSH"),
    "t3":                (80,  200,   "ng/dL",   "T3"),
    "t4":                (5.0, 12.0,  "µg/dL",   "T4"),
    "free t3":           (2.3, 4.2,   "pg/mL",   "Free T3"),
    "free t4":           (0.8, 1.8,   "ng/dL",   "Free T4"),

    # ── Electrolytes ──────────────────────────────────────────────────
    "sodium":            (136, 145,   "mEq/L",   "Sodium"),
    "potassium":         (3.5, 5.0,   "mEq/L",   "Potassium"),
    "chloride":          (98,  107,   "mEq/L",   "Chloride"),
    "bicarbonate":       (22,  29,    "mEq/L",   "Bicarbonate"),
    "calcium":           (8.5, 10.5,  "mg/dL",   "Calcium"),
    "phosphorus":        (2.5, 4.5,   "mg/dL",   "Phosphorus"),
    "magnesium":         (1.7, 2.4,   "mg/dL",   "Magnesium"),

    # ── Vitamins & Iron ───────────────────────────────────────────────
    "vitamin d":         (30,  100,   "ng/mL",   "Vitamin D"),
    "25-oh":             (30,  100,   "ng/mL",   "Vitamin D (25-OH)"),
    "vitamin b12":       (190, 900,   "pg/mL",   "Vitamin B12"),
    "b12":               (190, 900,   "pg/mL",   "Vitamin B12"),
    "folate":            (2.7, 17.0,  "ng/mL",   "Folate"),
    "ferritin":          (12,  300,   "ng/mL",   "Ferritin"),
    "serum iron":        (60,  170,   "µg/dL",   "Serum Iron"),
    "iron":              (60,  170,   "µg/dL",   "Serum Iron"),
    "tibc":              (240, 450,   "µg/dL",   "TIBC"),

    # ── Inflammatory / Other ──────────────────────────────────────────
    "crp":               (0,   1.0,   "mg/dL",   "C-Reactive Protein"),
    "c-reactive protein":(0,   1.0,   "mg/dL",   "C-Reactive Protein"),
    "esr":               (0,   20,    "mm/hr",   "ESR"),
    "psa":               (0,   4.0,   "ng/mL",   "PSA"),
    "hcg":               (0,   5.0,   "mIU/mL",  "hCG"),
}


def _lookup_reference(name: str) -> Tuple[Optional[float], Optional[float], str, str]:
    """Match a test name to the reference DB. Returns (min, max, unit, canonical_name)."""
    n = name.lower().strip()
    # Exact match
    if n in REFERENCE_DB:
        lo, hi, unit, canonical = REFERENCE_DB[n]
        return lo, hi, unit, canonical
    # Substring match (longest key that fits)
    best_key = None
    for key in REFERENCE_DB:
        if key in n or n in key:
            if best_key is None or len(key) > len(best_key):
                best_key = key
    if best_key:
        lo, hi, unit, canonical = REFERENCE_DB[best_key]
        return lo, hi, unit, canonical
    return None, None, "", name.strip().title()


# ── Regex patterns ─────────────────────────────────────────────────────────
# Pattern A: "TestName   12.5  g/dL   10.0 - 14.0"
_PAT_A = re.compile(
    r"^\s*(?P<test>[A-Za-z][A-Za-z0-9 \-/()%+\.]{2,40}?)\s+"
    r"(?P<value>-?\d+(?:\.\d+)?)"
    r"\s*(?P<unit>[A-Za-z/%µ^0-9]{1,12})?"
    r"[\s(]*"
    r"(?P<ref>(?:\d+(?:\.\d+)?\s*[-–to]+\s*\d+(?:\.\d+)?)|(?:[<>]\s*\d+(?:\.\d+)?))?",
    re.IGNORECASE,
)

# Pattern B: "TestName: 12.5 g/dL (10.0-14.0)"
_PAT_B = re.compile(
    r"^\s*(?P<test>[A-Za-z][A-Za-z0-9 \-/()%+\.]{2,40}?)\s*[:\-]\s*"
    r"(?P<value>-?\d+(?:\.\d+)?)"
    r"\s*(?P<unit>[A-Za-z/%µ^0-9]{1,12})?"
    r"[\s(]*"
    r"(?P<ref>(?:\d+(?:\.\d+)?\s*[-–to]+\s*\d+(?:\.\d+)?)|(?:[<>]\s*\d+(?:\.\d+)?))?",
    re.IGNORECASE,
)


def _parse_ref_str(ref: str) -> Tuple[Optional[float], Optional[float], str]:
    """
    Parse reference range text to (low, high, kind).
    kind: 'between' | 'less_than' | 'greater_than' | None
    """
    if not ref:
        return None, None, None

    s = ref.strip().lower()

    m = re.search(r"(\d+(?:\.\d+)?)\s*[-–to]+\s*(\d+(?:\.\d+)?)", s)
    if m:
        return float(m.group(1)), float(m.group(2)), "between"

    m = re.search(r"<\s*(\d+(?:\.\d+)?)", s)
    if m:
        return None, float(m.group(1)), "less_than"

    m = re.search(r">\s*(\d+(?:\.\d+)?)", s)
    if m:
        return float(m.group(1)), None, "greater_than"

    return None, None, None


def extract_parameters(cleaned_text: str) -> pd.DataFrame:
    """
    Stage 3: Parse cleaned text → structured DataFrame.

    Strategy:
      - Try Pattern A & B per line
      - For matched test names, enrich with reference DB
      - Deduplicate
    """
    rows = []
    seen = set()

    for raw_line in cleaned_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = None
        for pat in (_PAT_B, _PAT_A):
            m = pat.search(line)
            if m:
                match = m
                break

        if not match:
            continue

        gd = match.groupdict()
        raw_name  = (gd.get("test") or "").strip()
        value_str = (gd.get("value") or "").strip()
        unit_raw  = (gd.get("unit") or "").strip()
        ref_raw   = (gd.get("ref") or "").strip()

        if not raw_name or not value_str:
            continue

        try:
            value = float(value_str)
        except ValueError:
            continue

        # Skip lines that are clearly NOT test names
        skip_keywords = {
            "page", "name", "date", "patient", "lab", "result", "age",
            "sex", "gender", "id", "no", "dr", "ref", "unit", "time"
        }
        
        # Break the extracted name into individual words
        extracted_words = set(re.findall(r'\w+', raw_name.lower()))
        
        # If the extracted name contains ANY of the skip words, ignore it
        if len(raw_name) < 2 or extracted_words.intersection(skip_keywords):
            continue

        # Enrich with reference DB
        db_lo, db_hi, db_unit, canonical = _lookup_reference(raw_name)

        # Decide ref range: prefer inline, fall back to DB
        inline_lo, inline_hi, kind = _parse_ref_str(ref_raw)
        ref_lo  = inline_lo  if inline_lo  is not None else db_lo
        ref_hi  = inline_hi  if inline_hi  is not None else db_hi
        unit    = unit_raw   if unit_raw               else db_unit

        # Deduplicate by canonical name
        key = canonical.lower()
        if key in seen:
            continue
        seen.add(key)

        rows.append({
            "Test":            canonical,
            "Value":           value,
            "Unit":            unit,
            "Reference Range": f"{ref_lo} – {ref_hi}" if ref_lo and ref_hi else (ref_raw or "—"),
            "_ref_lo":         ref_lo,
            "_ref_hi":         ref_hi,
            "_ref_kind":       kind or ("between" if ref_lo and ref_hi else None),
        })

    if not rows:
        return pd.DataFrame(columns=["Test", "Value", "Unit",
                                     "Reference Range", "_ref_lo", "_ref_hi", "_ref_kind"])

    df = pd.DataFrame(rows).drop_duplicates(subset=["Test"])
    return df.reset_index(drop=True)


# ══════════════════════════════════════════════════════════════════════
# STAGE 4 — ABNORMAL DETECTION ENGINE
# ══════════════════════════════════════════════════════════════════════

def _compute_status(value: float, lo, hi, kind) -> str:
    if lo is None and hi is None:
        return "Unknown"
    if kind == "between":
        if value < lo:   return "Low"
        if value > hi:   return "High"
        return "Normal"
    if kind == "less_than":
        return "Normal" if value < hi else "High"
    if kind == "greater_than":
        return "Normal" if value > lo else "Low"
    return "Unknown"


def _compute_severity(value: float, lo, hi, status: str) -> str:
    if status in ("Normal", "Unknown"):
        return "None"
    if lo is None or hi is None:
        return "Moderate"
    span = abs(hi - lo)
    if span == 0:
        return "Moderate"
    deviation = abs(value - (lo if status == "Low" else hi)) / span
    if deviation < 0.2:  return "Mild"
    if deviation < 0.5:  return "Moderate"
    return "Severe"


def detect_abnormal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stage 4: Add Status and Severity columns.

    Status: Normal / High / Low / Unknown
    Severity: None / Mild / Moderate / Severe
    """
    if df.empty:
        return df

    df = df.copy()
    statuses, severities = [], []

    for _, row in df.iterrows():
        lo   = row.get("_ref_lo")
        hi   = row.get("_ref_hi")
        kind = row.get("_ref_kind")
        val  = row.get("Value")

        if val is None or (isinstance(val, float) and np.isnan(val)):
            statuses.append("Unknown")
            severities.append("None")
            continue

        status   = _compute_status(val, lo, hi, kind)
        severity = _compute_severity(val, lo, hi, status)
        statuses.append(status)
        severities.append(severity)

    df["Status"]   = statuses
    df["Severity"] = severities

    # Drop internal columns for display
    df_display = df.drop(columns=["_ref_lo", "_ref_hi", "_ref_kind"], errors="ignore")
    return df_display


# ══════════════════════════════════════════════════════════════════════
# STAGE 5 — RISK SCORING LAYER
# ══════════════════════════════════════════════════════════════════════

RISK_CATEGORIES = {
    "Diabetes Risk": {
        "tests":   ["Blood Glucose", "Fasting Blood Glucose", "Fasting Blood Sugar",
                    "Random Blood Sugar", "HbA1c", "Glycated Hemoglobin"],
        "icon":    "🩸",
        "insight": "Elevated glucose or HbA1c values may indicate impaired glucose tolerance.",
    },
    "Cardiovascular Risk": {
        "tests":   ["Total Cholesterol", "LDL Cholesterol", "HDL Cholesterol",
                    "Triglycerides", "VLDL"],
        "icon":    "❤️",
        "insight": "Abnormal lipid values are associated with increased cardiovascular risk.",
    },
    "Kidney Function": {
        "tests":   ["Creatinine", "Serum Creatinine", "BUN", "Blood Urea", "Uric Acid", "eGFR"],
        "icon":    "🫘",
        "insight": "Out-of-range kidney markers may indicate reduced kidney filtration.",
    },
    "Liver Function": {
        "tests":   ["SGPT (ALT)", "ALT", "SGOT (AST)", "AST", "Alkaline Phosphatase",
                    "ALP", "Bilirubin Total", "GGT"],
        "icon":    "🫀",
        "insight": "Elevated liver enzymes may reflect liver stress or inflammation.",
    },
    "Thyroid Health": {
        "tests":   ["TSH", "Free T3", "Free T4", "T3", "T4"],
        "icon":    "🦋",
        "insight": "Thyroid imbalances affect metabolism, energy, and mood.",
    },
    "Anaemia Risk": {
        "tests":   ["Hemoglobin", "Red Blood Cells", "Hematocrit", "Ferritin",
                    "Serum Iron", "MCV"],
        "icon":    "💉",
        "insight": "Low blood cell or iron values may indicate anaemia.",
    },
}


def compute_risk_scores(df: pd.DataFrame) -> List[dict]:
    """
    Stage 5: Derive risk category scores (0–100) from abnormal test counts.

    Returns a list of dicts with keys:
      category, icon, score, level, tests_found, tests_abnormal, insight
    """
    if df.empty:
        return []

    # Build name → status lookup (lowercase)
    name_status = {str(r["Test"]).lower(): r["Status"] for _, r in df.iterrows()}

    results = []
    for category, meta in RISK_CATEGORIES.items():
        relevant = [t for t in meta["tests"]
                    if t.lower() in name_status]
        if not relevant:
            continue

        n_abnormal = sum(1 for t in relevant if name_status[t.lower()] != "Normal")
        score = int((n_abnormal / len(relevant)) * 100)
        level = "low" if score < 30 else ("medium" if score < 65 else "high")

        results.append({
            "category":      category,
            "icon":          meta["icon"],
            "score":         score,
            "level":         level,
            "tests_found":   len(relevant),
            "tests_abnormal":n_abnormal,
            "insight":       meta["insight"],
        })

    return sorted(results, key=lambda x: -x["score"])


# ══════════════════════════════════════════════════════════════════════
# STAGE 6 — PERSONALISED EXPLANATION GENERATOR
# ══════════════════════════════════════════════════════════════════════

_EXPLANATIONS = {
    # Glucose
    "hemoglobin": {
        "high": "High hemoglobin can occur due to dehydration, smoking, or certain lung conditions. "
                "It does not always mean something serious, but your doctor should review it.",
        "low":  "Low hemoglobin is the most common sign of anaemia. You may feel tired, "
                "short of breath, or dizzy. Iron, B12, or folate deficiency are common causes. "
                "A doctor can determine the exact cause and recommend treatment.",
    },
    "blood glucose": {
        "high": "Higher-than-normal blood glucose may indicate pre-diabetes or diabetes. "
                "Diet, exercise, weight management, and (if advised) medications are key approaches.",
        "low":  "Low blood glucose (hypoglycaemia) can cause shakiness, confusion, or weakness. "
                "If you take diabetes medication, discuss this with your doctor promptly.",
    },
    "fasting blood sugar": {
        "high": "An elevated fasting glucose may suggest your body is having difficulty "
                "regulating blood sugar overnight. This warrants a follow-up with your doctor.",
        "low":  "A fasting glucose below normal is relatively uncommon and can cause symptoms. "
                "Please inform your doctor, especially if you feel unwell.",
    },
    "hba1c": {
        "high": "HbA1c reflects your average blood sugar over 3 months. A raised value suggests "
                "blood sugar has been consistently elevated, which is important to address.",
        "low":  "A low HbA1c may occur if you have had episodes of hypoglycaemia. "
                "Your doctor can advise on adjusting your management plan.",
    },
    "total cholesterol": {
        "high": "High total cholesterol may increase the risk of heart disease over time. "
                "A heart-healthy diet, exercise, and sometimes medication can help.",
        "low":  "Very low cholesterol is uncommon and usually not a concern, "
                "but your doctor should review it in context.",
    },
    "ldl cholesterol": {
        "high": "High LDL ('bad') cholesterol is a key risk factor for heart disease. "
                "Reducing saturated fats and increasing fibre can help lower it.",
        "low":  "Low LDL is generally positive for heart health.",
    },
    "hdl cholesterol": {
        "high": "High HDL ('good') cholesterol is generally protective for the heart.",
        "low":  "Low HDL may increase cardiovascular risk. Regular aerobic exercise "
                "and avoiding smoking can help raise HDL levels.",
    },
    "triglycerides": {
        "high": "High triglycerides are linked to heart and pancreas risk. "
                "Reducing sugar, refined carbs, and alcohol usually helps.",
        "low":  "Low triglycerides are generally considered healthy.",
    },
    "creatinine": {
        "high": "Elevated creatinine may indicate reduced kidney function. "
                "Staying well hydrated and avoiding nephrotoxic substances is important. "
                "Your doctor may request further kidney tests.",
        "low":  "Low creatinine can occur in people with low muscle mass. "
                "Usually not a concern on its own.",
    },
    "tsh": {
        "high": "High TSH suggests the thyroid gland may be underactive (hypothyroidism). "
                "Symptoms include fatigue, weight gain, and feeling cold. "
                "Thyroid hormone replacement therapy is effective.",
        "low":  "Low TSH may indicate an overactive thyroid (hyperthyroidism). "
                "Symptoms include weight loss, fast heartbeat, and anxiety. "
                "Your doctor will likely run further thyroid tests.",
    },
}

_LIFESTYLE_MAP = {
    "blood glucose": [
        "🥗 Choose low-glycaemic foods (vegetables, whole grains, legumes)",
        "🚶 Walk for at least 30 minutes daily",
        "💧 Drink 8+ glasses of water each day",
        "⚖️ Maintain a healthy weight",
        "🧘 Manage stress — it affects blood sugar",
    ],
    "cholesterol": [
        "🥦 Eat more soluble fibre (oats, apples, beans)",
        "🐟 Include omega-3 rich foods (salmon, walnuts, flaxseeds)",
        "🧈 Reduce saturated and trans fats",
        "🚴 Exercise most days of the week",
        "🚭 Avoid smoking",
    ],
    "hemoglobin": [
        "🥩 Eat iron-rich foods (spinach, lean red meat, lentils)",
        "🍊 Pair iron foods with vitamin C to boost absorption",
        "🩺 Ask your doctor about iron supplements if needed",
        "🥚 Include B12 sources (eggs, dairy, fish)",
    ],
    "creatinine": [
        "💧 Stay well hydrated throughout the day",
        "🧂 Limit high-salt, high-protein processed foods",
        "🚫 Avoid unnecessary pain-killer overuse (NSAIDs)",
        "🩺 Get kidney function monitored regularly",
    ],
    "tsh": [
        "😴 Prioritise 7–9 hours of sleep nightly",
        "🧘 Practice stress management (yoga, meditation)",
        "💊 Take prescribed thyroid medication consistently",
        "🩺 Get thyroid levels re-tested as your doctor advises",
    ],
}

_GENERIC_LIFESTYLE = [
    "😴 Get 7–8 hours of quality sleep each night",
    "💧 Stay hydrated — drink 8 glasses of water daily",
    "🥗 Eat a balanced diet with plenty of fruits and vegetables",
    "🚶 Be physically active for at least 30 minutes most days",
    "🧘 Manage stress through mindfulness, hobbies, or social connection",
    "🩺 Keep regular follow-up appointments with your doctor",
    "🚭 Avoid smoking and limit alcohol",
]


def generate_summary(
    df: pd.DataFrame,
    age: Optional[int] = None,
    gender: str = "Not specified",
) -> dict:
    """
    Stage 6: Produce a plain-language summary with findings and lifestyle suggestions.
    Tone adapts based on age (senior-friendly if age >= 60).
    """
    if df.empty:
        return {
            "heading": "No Data Extracted",
            "description": "We could not identify any lab values from this report. "
                           "The file may be unclear or in an unsupported format.",
            "findings": [],
            "lifestyle": _GENERIC_LIFESTYLE,
            "total": 0,
            "abnormal_count": 0,
            "normal_count": 0,
        }

    total         = len(df)
    is_senior     = (age or 0) >= 60
    senior_prefix = "In simple terms: " if is_senior else ""

    abnormal_df = df[df["Status"].isin(["High", "Low"])]
    n_abnormal  = len(abnormal_df)
    n_normal    = total - n_abnormal

    # Heading
    if n_abnormal == 0:
        heading = "All Values Within Normal Range"
        description = (
            f"{senior_prefix}Your report shows {total} test values. "
            "All of them are within the expected reference ranges. "
            "This is a positive result. Continue your healthy habits and "
            "attend routine check-ups with your doctor."
        )
    elif n_abnormal == 1:
        heading = "One Value Needs Attention"
        description = (
            f"{senior_prefix}Your report shows {total} values. "
            "One result is outside the normal range. This alone may not be serious, "
            "but it is worth discussing with your doctor."
        )
    else:
        heading = f"{n_abnormal} Values Need Attention"
        description = (
            f"{senior_prefix}Your report shows {total} values — "
            f"{n_normal} are normal and {n_abnormal} are outside the expected range. "
            "Please share this report with your doctor for proper evaluation."
        )

    # Per-test findings
    findings = []
    lifestyle_keys = set()

    for _, row in abnormal_df.iterrows():
        name      = str(row["Test"])
        status    = row["Status"]
        value     = row["Value"]
        unit      = row.get("Unit", "")
        ref_range = row.get("Reference Range", "—")
        severity  = row.get("Severity", "")

        direction = "lower" if status == "Low" else "higher"
        sev_word  = {"Mild": "slightly", "Moderate": "notably",
                     "Severe": "significantly"}.get(severity, "")

        name_key = name.lower()
        expl = ""
        for key, vals in _EXPLANATIONS.items():
            if key in name_key:
                expl = vals.get(status.lower(), "")
                # Collect lifestyle keys
                for lkey in _LIFESTYLE_MAP:
                    if lkey in name_key:
                        lifestyle_keys.add(lkey)
                break

        findings.append({
            "name":      name,
            "status":    status,
            "value":     value,
            "unit":      unit,
            "ref_range": ref_range,
            "direction": direction,
            "severity":  sev_word,
            "explanation": expl,
        })

    # Lifestyle suggestions
    lifestyle = []
    for lk in lifestyle_keys:
        lifestyle.extend(_LIFESTYLE_MAP.get(lk, []))
    if not lifestyle:
        lifestyle = _GENERIC_LIFESTYLE.copy()
    else:
        lifestyle += [_GENERIC_LIFESTYLE[-2], _GENERIC_LIFESTYLE[-1]]  # always add doctor tip

    return {
        "heading":       heading,
        "description":   description,
        "findings":      findings,
        "lifestyle":     list(dict.fromkeys(lifestyle)),  # deduplicate, preserve order
        "total":         total,
        "abnormal_count": n_abnormal,
        "normal_count":  n_normal,
    }
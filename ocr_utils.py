"""
ocr_utils.py
Stage 1 & 2: OCR Engine + Text Cleaning
─────────────────────────────────────────
Handles text extraction from:
  - Text-based PDFs    → pdfplumber (fast, accurate)
  - Scanned PDFs       → pdf2image → OpenCV → pytesseract
  - Images (JPG/PNG)   → OpenCV → pytesseract

Text cleaning:
  - Normalise line endings
  - Strip noise characters
  - Collapse whitespace
"""

import io
import re
import numpy as np
from typing import Tuple

# Graceful imports — app works in degraded mode if a library is missing
try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import cv2
    CV2_OK = True
except ImportError:
    CV2_OK = False

try:
    import pdfplumber
    PDFPLUMBER_OK = True
except ImportError:
    PDFPLUMBER_OK = False

try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_OK = True
except ImportError:
    PDF2IMAGE_OK = False

try:
    import pytesseract
    TESSERACT_OK = True
except ImportError:
    TESSERACT_OK = False


# ══════════════════════════════════════════════════════════════════════
# IMAGE PREPROCESSING
# ══════════════════════════════════════════════════════════════════════

def preprocess_image(pil_image) -> object:
    """
    OpenCV preprocessing pipeline for OCR accuracy:
      1. Convert to RGB (normalize modes)
      2. Grayscale
      3. Upscale to target width (helps on small text)
      4. Gaussian denoise
      5. Adaptive threshold (handles uneven lighting)

    Returns preprocessed numpy array (grayscale).
    """
    if not CV2_OK or not PIL_OK:
        return pil_image  # return as-is for direct Tesseract use

    # Ensure RGB
    image = pil_image.convert("RGB")
    img_np = np.array(image)

    # Grayscale
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # Upscale for clarity (target 1600px wide)
    target_width = 1600
    h, w = gray.shape
    if w < target_width:
        scale = target_width / w
        gray = cv2.resize(gray, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_CUBIC)

    # Mild denoise
    gray = cv2.GaussianBlur(gray, (1, 1), 0)

    # Adaptive threshold for non-uniform scan backgrounds
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 15,
    )
    return thresh


def _ocr_numpy(arr) -> str:
    """Run Tesseract on a preprocessed numpy image array."""
    if not TESSERACT_OK:
        return ""
    config = "--oem 3 --psm 6"
    try:
        return pytesseract.image_to_string(arr, lang="eng", config=config)
    except Exception as e:
        return f"[Tesseract error: {e}]"


# ══════════════════════════════════════════════════════════════════════
# PDF EXTRACTION
# ══════════════════════════════════════════════════════════════════════

def _extract_pdf_text(file_bytes: bytes) -> Tuple[str, str]:
    """
    Try pdfplumber first; fall back to OCR for scanned PDFs.
    Returns (text, method_description).
    """
    text = ""

    # ── Attempt 1: pdfplumber (text-based PDF) ────────────────────
    if PDFPLUMBER_OK:
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                parts = []
                for page in pdf.pages:
                    pt = page.extract_text() or ""
                    parts.append(pt)
                text = "\n".join(parts)
        except Exception:
            text = ""

        if len(text.strip()) >= 50:
            return text, "pdfplumber (digital text)"

    # ── Attempt 2: pdf2image + OCR (scanned PDF) ─────────────────
    if PDF2IMAGE_OK and PIL_OK and TESSERACT_OK:
        try:
            images = convert_from_bytes(file_bytes, dpi=220, fmt="ppm")
            parts = []
            for img in images:
                processed = preprocess_image(img)
                parts.append(_ocr_numpy(processed))
            return "\n".join(parts), "pdf2image + OpenCV + Tesseract"
        except Exception as e:
            return f"[PDF OCR failed: {e}]", "failed"

    return text, "pdfplumber (partial)"


# ══════════════════════════════════════════════════════════════════════
# IMAGE EXTRACTION
# ══════════════════════════════════════════════════════════════════════

def _extract_image_text(file_bytes: bytes) -> Tuple[str, str]:
    """Extract text from a JPG/PNG image via OpenCV preprocessing."""
    if not PIL_OK:
        return "", "PIL not installed"
    try:
        img = Image.open(io.BytesIO(file_bytes))
        processed = preprocess_image(img)
        text = _ocr_numpy(processed)
        return text, "OpenCV + Tesseract"
    except Exception as e:
        return f"[Image error: {e}]", "failed"


# ══════════════════════════════════════════════════════════════════════
# MAIN EXTRACT FUNCTION
# ══════════════════════════════════════════════════════════════════════

def extract_text(uploaded_file) -> Tuple[str, str]:
    """
    Stage 1: Extract raw text from an uploaded file.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        (raw_text, method_used)
    """
    if uploaded_file is None:
        return "", "no file"

    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_pdf_text(file_bytes)

    if filename.endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp")):
        return _extract_image_text(file_bytes)

    return "", "unsupported format"


# ══════════════════════════════════════════════════════════════════════
# TEXT CLEANING (STAGE 2)
# ══════════════════════════════════════════════════════════════════════

def clean_text(raw_text: str) -> str:
    """
    Stage 2: Normalise and clean OCR-extracted text.

    Operations:
      - Normalise line endings
      - Strip control characters (except newlines/tabs)
      - Collapse multi-space runs (preserve newlines)
      - Trim trailing whitespace per line
      - Collapse 3+ consecutive blank lines to 2
      - Strip surrounding whitespace
    """
    if not raw_text:
        return ""

    # Normalise newlines
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove non-printable characters (keep \n \t)
    text = re.sub(r"[^\S\n\t]+", " ", text)

    # Trim trailing space before newlines
    text = re.sub(r"[ \t]+\n", "\n", text)

    # Collapse 3+ blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove obvious OCR garbage lines (single character lines of noise)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        # Keep if: non-empty, not just punctuation/symbols, has at least one letter or digit
        if stripped and re.search(r"[A-Za-z0-9]", stripped):
            lines.append(line)
        elif not stripped:
            lines.append("")  # preserve blank separator lines

    return "\n".join(lines).strip()


# ══════════════════════════════════════════════════════════════════════
# DEPENDENCY STATUS
# ══════════════════════════════════════════════════════════════════════

def get_dependency_status() -> dict:
    """Return availability of each OCR library."""
    return {
        "Pillow (PIL)": PIL_OK,
        "OpenCV":       CV2_OK,
        "pdfplumber":   PDFPLUMBER_OK,
        "pdf2image":    PDF2IMAGE_OK,
        "pytesseract":  TESSERACT_OK,
    }

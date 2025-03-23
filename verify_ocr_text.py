
import pytesseract
import cv2
import re

def extract_text_tesseract(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return ""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()

def clean_ocr_text(text):
    return re.sub(r'[^a-zA-Z0-9 /-]', '', text).strip()

def verify_ocr_text(image_path, known_terms=None):
    raw_text = extract_text_tesseract(image_path)
    cleaned = clean_ocr_text(raw_text)
    if known_terms:
        matches = [term for term in known_terms if term.lower() in cleaned.lower()]
        return max(matches, key=len) if matches else cleaned
    return cleaned

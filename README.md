
# 🧠 Trading Card AI: Smart Labeling & Listing Pipeline

This project is a full intelligent automation system for detecting, labeling, describing, pricing, and correcting trading cards using YOLOv8 + LLM-inspired logic.

---

## 📁 Project Structure

```
trading-card-ai/
├── datasets/
│   ├── train/images/
│   ├── train/labels/
│   ├── val/images/
│   ├── val/labels/
│   ├── test/images/
│   ├── test/labels/
│   └── feedback/corrections.json
├── models/
│   └── parallel_detector_v1.pt
├── multi_infer_yolo.py
├── verify_class_llm.py
├── auto_label.py
├── verify_ocr_text.py
├── generate_listings.py
├── rank_listings_llm.py
├── crowd_feedback_loop.py
└── train.yaml
```

---

## ✅ Key Scripts

| File | Description |
|------|-------------|
| `multi_infer_yolo.py` | Runs YOLO multiple times per image with augmentations |
| `verify_class_llm.py` | Verifies the best prediction using rules and metadata |
| `auto_label.py` | Uses the above two scripts to generate YOLO training labels |
| `verify_ocr_text.py` | Extracts and validates OCR text (e.g., player name, serial) |
| `generate_listings.py` | Builds listing title, description, and price |
| `rank_listings_llm.py` | Chooses the best version of a listing |
| `crowd_feedback_loop.py` | Records and retrieves user label corrections |

---

## 🚀 How to Use

### 1. Label Cards Automatically

```bash
python auto_label.py
```

### 2. Validate Labels

```bash
yolo detect val model=yolov8n.pt data=datasets/train.yaml
```

### 3. Train YOLO

```bash
yolo train model=yolov8n.pt data=datasets/train.yaml epochs=50 imgsz=640
```

### 4. Extract OCR Text from Cards

```python
from verify_ocr_text import verify_ocr_text
text = verify_ocr_text("datasets/train/images/sample.jpg", known_terms=["LeBron", "Curry"])
```

### 5. Generate and Rank Listings

```python
from generate_listings import generate_listing
from rank_listings_llm import rank_listings

candidates = [generate_listing(card_data) for _ in range(3)]
best = rank_listings(candidates, required_terms=["Gold Prizm", "LeBron"])
print(best)
```

### 6. Capture Feedback for Retraining

```python
from crowd_feedback_loop import record_correction

record_correction("LeBron_Gold_Prizm.jpg", original_class_id=4, suggested_class_id=6, reason="should be Blue Wave")
```

---

## 🧩 Requirements

```bash
pip install ultralytics opencv-python pytesseract pyyaml
```

---

## ❤️ Contribute

PRs welcome for:
- Ensembling multiple YOLO models
- GPT-assisted OCR logic
- Advanced listing generation via LLM

Built to serve collectors, graders, and AI enthusiasts!

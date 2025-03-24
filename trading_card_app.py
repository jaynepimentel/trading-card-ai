
import streamlit as st
from PIL import Image
from multi_infer_yolo import run_multi_infer
from verify_class_llm import verify_best_class, load_classes_from_yaml
from verify_ocr_text import verify_ocr_text
from generate_listings import generate_listing
from rank_listings_llm import rank_listings
from crowd_feedback_loop import record_correction

MODEL_PATH = "detect/train17/weights/best.pt"
DATA_YAML = "datasets/train.yaml"
CLASS_NAMES = load_classes_from_yaml(DATA_YAML)

st.set_page_config(page_title="Trading Card AI", layout="centered")

st.title("🧠 Trading Card AI")

uploaded_file = st.file_uploader("Upload a card image", type=["jpg", "png"])
class_id = None  # Ensures it's defined before use

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Card", use_container_width=True)  # Modern width usage
    image_path = f"temp_{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.subheader("🔍 Auto Classification")
    predictions = run_multi_infer(MODEL_PATH, image_path)
    class_id = verify_best_class(predictions, uploaded_file.name, CLASS_NAMES)

if class_id is None:
    st.error("❌ No confident prediction was made by the model.")
else:
    st.success(f"Predicted Class: {CLASS_NAMES[class_id]}")

    st.subheader("🔡 OCR Extraction")
    extracted_text = verify_ocr_text(image_path)
    st.code(extracted_text, language="text")

    st.subheader("🛒 Listing Generator")
    card_data = {
        'player': extracted_text if extracted_text else "Unknown",
        'set': "2024 Panini Prizm",
        'parallel': CLASS_NAMES[class_id],
        'condition': 'Near Mint',
        'serial': '/XX',
        'year': '2024'
    }
    candidates = [generate_listing(card_data) for _ in range(3)]
    best = rank_listings(candidates, required_terms=[CLASS_NAMES[class_id]])

    st.write("### 🏆 Best Listing")
    st.text_area("Title", value=best['title'], height=40)
    st.text_area("Description", value=best['description'], height=120)
    st.write(f"💰 Estimated Price: **${best['estimated_price']}**")

    st.subheader("🗳 Submit Correction (Optional)")
    with st.form("feedback_form"):
        suggested_class = st.selectbox("Suggest a better class:", CLASS_NAMES)
        reason = st.text_input("Why is this class better?")
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            record_correction(uploaded_file.name, class_id, CLASS_NAMES.index(suggested_class), reason)
            st.success("Feedback submitted!")

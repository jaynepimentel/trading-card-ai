
import json
import os

FEEDBACK_LOG = "datasets/feedback/corrections.json"
os.makedirs(os.path.dirname(FEEDBACK_LOG), exist_ok=True)

def record_correction(image_name, original_class_id, suggested_class_id, reason=""):
    feedback = {
        "image": image_name,
        "original_class": original_class_id,
        "suggested_class": suggested_class_id,
        "reason": reason
    }
    if os.path.exists(FEEDBACK_LOG):
        with open(FEEDBACK_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(feedback)
    with open(FEEDBACK_LOG, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Feedback saved for {image_name}")

def get_feedback_entries():
    if not os.path.exists(FEEDBACK_LOG):
        return []
    with open(FEEDBACK_LOG, "r") as f:
        return json.load(f)

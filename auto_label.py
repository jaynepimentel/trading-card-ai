
import os
from multi_infer_yolo import run_multi_infer
from verify_class_llm import verify_best_class, load_classes_from_yaml

MODEL_PATH = "models/parallel_detector_v1.pt"
IMAGE_DIR = "datasets/train/images"
LABEL_DIR = "datasets/train/labels"
DATA_YAML = "datasets/train.yaml"

os.makedirs(LABEL_DIR, exist_ok=True)
class_names = load_classes_from_yaml(DATA_YAML)

def auto_label_dataset():
    for filename in os.listdir(IMAGE_DIR):
        if not filename.lower().endswith(".jpg"):
            continue
        image_path = os.path.join(IMAGE_DIR, filename)
        predictions = run_multi_infer(MODEL_PATH, image_path, n=5)
        if not predictions:
            print(f"⚠️ No predictions for {filename}")
            continue
        class_id = verify_best_class(predictions, filename, class_names)
        if class_id is None:
            print(f"❌ Could not verify label for {filename}")
            continue
        label_path = os.path.join(LABEL_DIR, filename.replace(".jpg", ".txt"))
        with open(label_path, "w") as f:
            f.write(f"{class_id} 0.5 0.5 0.714 1.0\n")
        print(f"✅ Labeled {filename} as {class_names[class_id]}")

if __name__ == "__main__":
    auto_label_dataset()


import os
import yaml

def load_classes_from_yaml(yaml_path):
    with open(yaml_path, "r") as file:
        data = yaml.safe_load(file)
    return data.get("names", [])

def verify_best_class(predictions, image_filename, class_names, metadata=None):
    filename_lower = image_filename.lower()
    fallback = predictions[0][0] if predictions else None

    for class_id, votes in predictions:
        class_name = class_names[class_id].lower()
        if class_name.replace(" ", "_") in filename_lower or class_name in filename_lower:
            return class_id
        if metadata:
            set_info = metadata.get("set", "").lower()
            if class_name in set_info:
                return class_id
    return fallback

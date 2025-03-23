
from ultralytics import YOLO
import cv2
import numpy as np
import os

def augment_image(image, index):
    if index % 2 == 0:
        return cv2.GaussianBlur(image, (5, 5), 0)
    elif index % 3 == 0:
        return cv2.convertScaleAbs(image, alpha=1.05, beta=10)
    elif index % 5 == 0:
        return cv2.flip(image, 1)
    else:
        return image

def run_multi_infer(model_path, image_path, n=5):
    model = YOLO(model_path)
    image = cv2.imread(image_path)
    class_votes = {}

    for i in range(n):
        aug_img = augment_image(image.copy(), i)
        result = model.predict(aug_img, imgsz=640, conf=0.25)[0]
        for box in result.boxes:
            class_id = int(box.cls.item())
            class_votes[class_id] = class_votes.get(class_id, 0) + 1

    return sorted(class_votes.items(), key=lambda x: x[1], reverse=True)

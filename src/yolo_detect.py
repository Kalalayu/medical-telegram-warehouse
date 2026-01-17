from ultralytics import YOLO
import os
import pandas as pd

IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/processed/image_detections.csv"

model = YOLO("yolov8n.pt")

results_data = []

for channel in os.listdir(IMAGE_DIR):
    channel_path = os.path.join(IMAGE_DIR, channel)

    if not os.path.isdir(channel_path):
        continue

    for image_file in os.listdir(channel_path):
        image_path = os.path.join(channel_path, image_file)

        try:
            detections = model(image_path)[0]
            labels = detections.names
            detected_classes = [labels[int(c)] for c in detections.boxes.cls]
            confidences = detections.boxes.conf.tolist()

            has_person = "person" in detected_classes
            has_product = any(obj in detected_classes for obj in ["bottle", "box", "cup"])

            if has_person and has_product:
                category = "promotional"
            elif has_product:
                category = "product_display"
            elif has_person:
                category = "lifestyle"
            else:
                category = "other"

            message_id = image_file.split(".")[0]

            results_data.append({
                "message_id": message_id,
                "channel_name": channel,
                "detected_class": ",".join(set(detected_classes)),
                "confidence_score": max(confidences) if confidences else None,
                "image_category": category
            })

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

df = pd.DataFrame(results_data)
df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved detections to {OUTPUT_CSV}")

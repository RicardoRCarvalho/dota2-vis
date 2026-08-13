from ultralytics import YOLO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model = YOLO("yolo11n.yaml")

# Train the model
model.train(data=BASE_DIR / "data.yaml", epochs=200, patience=15, imgsz=480, max_det=40, dropout=0.1, iou=0.35, auto_augment=None, hsv_h=0, hsv_s=0.1, hsv_v=0.2, flipud=0.1, mosaic=0.2, shear=5, degrees=5, perspective=0.00025, scale=0.2, erasing=0.1)

# Validate
model.val()
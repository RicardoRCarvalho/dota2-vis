import os
from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

class_map = {
    1 : "P1",
    3 : "P2",
    5 : "P3",
    7 : "P4",
    9 : "P5",
    11 : "X1",
    13 : "X2",
    15 : "X3",
    17 : "X4",
    19 : "X5",
}

#target_IDs = [11, 13, 15, 17, 19] Radiant Vision detecting Dire Players
target_IDs = [1, 3, 5, 7, 9] #Dire Vision detecting Radiant Players

MODEL_PATH = BASE_DIR / "YOLO/best.pt"
model = YOLO(MODEL_PATH)


#timer coordinates
y_start = 0
y_end = 40
x_start = 900
x_end = 1020

#timer regions
regions = [
    (35, 24, 9, 11),   # H1
    (44, 24, 9, 11),   # H2
    (57, 24, 9, 11),   # M1
    (66, 24, 9, 11)    # M2
]

template_folder = BASE_DIR / "digit_templates_flat"

templates = []  # List of (label, image)

for fname in os.listdir(template_folder):
    if not fname.endswith('.jpg'):
        continue
    parts = fname.split('_')
    if len(parts) != 3:
        continue
    _, _, label = parts
    label = label.split('.')[0]
    tmpl_path = os.path.join(template_folder, fname)
    tmpl_img = cv2.imread(tmpl_path, cv2.IMREAD_GRAYSCALE)
    if tmpl_img is None:
        continue
    elif len(tmpl_img.shape) == 3:
        tmpl_img = tmpl_img.squeeze()
        templates.append((label, tmpl_img))

#minimap regions
y2_start = 840
y2_end = 1080
x2_start = 1680
x2_end = 1920

registros = []
step = 0
time_count = 0

last_prediction = 9999
current_prediction = 9999

#DELETAR DEPOIS
count = 0

VIDEO_PATH = BASE_DIR / "TI_Aurora Gaming_x_BetBoom Team_Group StageGame 1_Dire vision.mkv"

cap = cv2.VideoCapture(VIDEO_PATH, cv2.CAP_FFMPEG)
processed_frames = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret or frame is None:
        break

    processed_frames += 1

    minimap = frame[y2_start:y2_end, x2_start:x2_end]
    current_time = frame[y_start:y_end, x_start:x_end]


    if processed_frames % 15 != 0:
        continue


    gray = cv2.cvtColor(current_time, cv2.COLOR_BGR2GRAY)


    # Predict time
    pred_chars = []
    for i, (x, y, w, h) in enumerate(regions):
        crop = gray[y:y+h, x:x+w]

        best_score = -np.inf
        best_label = None
        for label, tmpl in templates:
            if tmpl.shape != crop.shape:
                continue
            res = cv2.matchTemplate(crop, tmpl, cv2.TM_CCOEFF_NORMED)
            score = res[0][0]
            if score > best_score:
                best_score = score
                best_label = label

        pred_chars.append(best_label if best_label else '?')

    # Post-processing
    pred_chars = ['0' if ch == '#' else ch for ch in pred_chars]
    pred_str = ''.join(pred_chars)


    #Se tiver mais que 2 predições de tempo iguais, deduz que é pause e ignora proximas leituras com mesmo tempo até predição diferente
    if(last_prediction == current_prediction and current_prediction == int(pred_str)):
        print("pause " + pred_str)
        continue
    else:
        last_prediction = current_prediction
        current_prediction = int(pred_str)


    if(int(pred_str) == 45 and step == 0):
        step += 1 #Primeiros 00:45 (Contagem regressiva)
        time_range = "00:45 - 00:00"
    elif(int(pred_str)//500 == time_count):
        print(f"count: {time_count} pred:  + {int(pred_str)} step: {step}")
        time_count += 1
        time_range = str((time_count-1)*500) + " - " + str(time_count*500)
        step += 1
    elif(int(pred_str) == 0 and time_count > 1):
        # 4-digit time(>=10min)
        regions = [
            (40, 24, 9, 11),   # H1
            (49, 24, 9, 11),   # H2
            (63, 24, 8, 11),   # M1
            (72, 24, 8, 11)    # M2
        ]
        time_count += 1
        time_range = str((time_count-1)*500) + " - " + str(time_count*500)
    if(step > 0):
        results = model.track(
            minimap,
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.3,
            iou=0.5,
            verbose=False
        )
        detected_ids = set()
        if results[0].boxes.id is not None:
            boxes = results[0].boxes

            for cls in boxes.cls:
                detected_ids.add(int(cls))
            for box, cls in zip(boxes.xyxy, boxes.cls):

                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(
                        minimap,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        minimap,
                        class_map.get(int(cls)),
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        1
                    )
        # Now iterate over ALL target IDs
        for target_id in target_IDs:
            visivel = 1 if target_id in detected_ids else 0
            registros.append({
                "jogador": class_map.get(target_id),
                "frame": processed_frames,
                "visivel": visivel,
                "range": time_range,
                "prediction": pred_str
                            })

        #DELETAR DEPOIS
        count += 1
        #print(f"Count: {count}")
        if count == 10:
            #cv2_imshow(minimap)
            print(f'Prediction: {pred_str}')
            print(f"frame= {processed_frames}")
            print(f"range = {time_range}")
            count = 0

cap.release()
cv2.destroyAllWindows()
df = pd.DataFrame(registros)
df.to_csv(str(BASE_DIR) + "/visibilidade_TI_Aurora Gaming_x_BetBoom Team_Group StageGame 1_Dire.csv", index=False)
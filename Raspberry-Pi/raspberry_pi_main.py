import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import time
import threading
import numpy as np
import cv2
import serial

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_edge_litert.interpreter import Interpreter
from picamera2 import Picamera2
from ultralytics import YOLO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arduino
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)
    print("Arduino connected")
except:
    arduino = None
    print("Arduino not connected")

latest_result = {
    "ready": False,
    "locked": False,
    "type": "",
    "fruit": "",
    "disease": "",
    "confidence": 0,
    "info": ""
}

YOLO_CONF = 0.50
YOLO_IMGSZ = 160
YOLO_EVERY_N_FRAMES = 20

DISEASE_CONF_LIMIT = 20
CONFIRM_SECONDS = 1

zoom_factor = 2.0
locked = False
frame_count = 0

last_disease = None
start_confirm_time = None

plant_detected_cached = False
plant_conf_cached = 0

plant_detector = YOLO("/home/alawneh/Downloads/best (1).pt")

disease_interpreter = Interpreter(
    model_path="/home/alawneh/Downloads/fruit_disease_modelnew.tflite"
)

disease_interpreter.allocate_tensors()

disease_input_details = disease_interpreter.get_input_details()
disease_output_details = disease_interpreter.get_output_details()

with open("/home/alawneh/Downloads/Newclasses.txt", "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]


def send_to_arduino(msg):
    global arduino

    try:
        if arduino is not None:
            arduino.write((msg + "\n").encode())
            print("Sent to Arduino:", msg)
        else:
            print("Arduino is not connected")
    except Exception as e:
        print("Arduino send error:", e)


def get_fruit_type(disease_name):
    name = disease_name.lower().strip()
    parts = name.split("_")

    if len(parts) >= 2:
        return parts[-1]

    return name


def send_fruit_to_arduino(fruit_type):
    fruit = fruit_type.lower().strip()

    send_to_arduino("plant")
    time.sleep(0.3)

    if fruit == "apple":
        send_to_arduino("apple")

    elif fruit == "guava":
        send_to_arduino("guava")

    elif fruit == "pomegranate":
        send_to_arduino("pomegranate")

    else:
        print("Unknown fruit:", fruit)


def zoom_frame(frame, zoom_factor):
    h, w = frame.shape[:2]

    new_w = int(w / zoom_factor)
    new_h = int(h / zoom_factor)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2

    crop = frame[y1:y1 + new_h, x1:x1 + new_w]

    return cv2.resize(crop, (w, h))


def preprocess_square(img, size=224):
    h, w = img.shape[:2]
    max_size = max(h, w)

    square = np.zeros((max_size, max_size, 3), dtype=np.uint8)

    y_offset = (max_size - h) // 2
    x_offset = (max_size - w) // 2

    square[y_offset:y_offset + h, x_offset:x_offset + w] = img

    return cv2.resize(square, (size, size))


def detect_plant(frame_bgr):
    results = plant_detector.predict(
        source=frame_bgr,
        imgsz=YOLO_IMGSZ,
        conf=YOLO_CONF,
        verbose=False
    )

    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return False, 0

    best_conf = 0

    for box in boxes:
        conf = float(box.conf[0])
        if conf > best_conf:
            best_conf = conf

    return True, best_conf * 100


def predict_disease(frame_bgr):
    processed_img = preprocess_square(frame_bgr, 224)

    input_img = processed_img.astype(np.float32)
    input_img = np.expand_dims(input_img, axis=0)

    disease_interpreter.set_tensor(
        disease_input_details[0]["index"],
        input_img
    )

    disease_interpreter.invoke()

    predictions = disease_interpreter.get_tensor(
        disease_output_details[0]["index"]
    )

    predicted_class = int(np.argmax(predictions))
    disease_name = class_names[predicted_class]
    confidence = float(np.max(predictions) * 100)

    return disease_name, confidence


def get_disease_info(disease_name):
    return f"""
اسم المرض: {disease_name}

تم اكتشاف الحالة بواسطة المودل.
"""


def reset_all():
    global latest_result
    global locked
    global frame_count
    global last_disease
    global start_confirm_time
    global plant_detected_cached
    global plant_conf_cached

    locked = False
    frame_count = 0
    last_disease = None
    start_confirm_time = None
    plant_detected_cached = False
    plant_conf_cached = 0

    latest_result = {
        "ready": False,
        "locked": False,
        "type": "",
        "fruit": "",
        "disease": "",
        "confidence": 0,
        "info": ""
    }


def camera_loop():
    global latest_result
    global zoom_factor
    global locked
    global frame_count
    global last_disease
    global start_confirm_time
    global plant_detected_cached
    global plant_conf_cached

    picam2 = Picamera2()

    picam2.configure(
        picam2.create_preview_configuration(
            main={
                "size": (640, 480),
                "format": "BGR888"
            }
        )
    )

    picam2.start()

    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera", 1000, 700)

    while True:
        frame_bgr = picam2.capture_array()

        frame_bgr = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        frame_bgr = zoom_frame(frame_bgr, zoom_factor)

        if not locked:
            frame_count += 1

            if frame_count % YOLO_EVERY_N_FRAMES == 0:
                plant_detected_cached, plant_conf_cached = detect_plant(frame_bgr)

            if not plant_detected_cached:
                latest_result = {
                    "ready": False,
                    "locked": False,
                    "type": "No Plant",
                    "fruit": "",
                    "disease": "",
                    "confidence": 0,
                    "info": "لم يتم اكتشاف نبتة أو ثمرة."
                }

                last_disease = None
                start_confirm_time = None
                text = "No plant detected"

            else:
                disease_name, confidence = predict_disease(frame_bgr)

                # أول ما يشوف نبتة وقف السيارة
                send_to_arduino("plant")

                if confidence >= DISEASE_CONF_LIMIT:
                    if disease_name == last_disease:
                        elapsed = time.time() - start_confirm_time

                        if elapsed >= CONFIRM_SECONDS:
                            locked = True

                            fruit_type = get_fruit_type(disease_name)
                            disease_info = get_disease_info(disease_name)

                            # إرسال نوع الفاكهة للأردوينو
                            send_fruit_to_arduino(fruit_type)

                            latest_result = {
                                "ready": True,
                                "locked": True,
                                "type": "Plant",
                                "fruit": fruit_type,
                                "disease": disease_name,
                                "confidence": round(confidence, 1),
                                "info": disease_info
                            }

                    else:
                        last_disease = disease_name
                        start_confirm_time = time.time()

                else:
                    last_disease = None
                    start_confirm_time = None

                text = (
                    f"Plant {plant_conf_cached:.1f}% | "
                    f"{disease_name} {confidence:.1f}%"
                )

        else:
            text = f"LOCKED: {latest_result['disease']}"

        cv2.putText(
            frame_bgr,
            text,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0) if plant_detected_cached else (0, 0, 255),
            2
        )

        cv2.putText(
            frame_bgr,
            f"Zoom: {zoom_factor:.1f}x",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        cv2.imshow("Camera", frame_bgr)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('+') or key == ord('='):
            zoom_factor += 0.2
            if zoom_factor > 5.0:
                zoom_factor = 5.0

        elif key == ord('-'):
            zoom_factor -= 0.2
            if zoom_factor < 1.0:
                zoom_factor = 1.0

        elif key == ord('r'):
            reset_all()

    picam2.stop()
    cv2.destroyAllWindows()


@app.get("/")
def home():
    return {
        "message": "Raspberry API is working"
    }


@app.get("/result")
def get_result():
    return latest_result


@app.get("/reset")
def reset_result():
    reset_all()
    return {
        "reset": True
    }


threading.Thread(
    target=camera_loop,
    daemon=True
).start()

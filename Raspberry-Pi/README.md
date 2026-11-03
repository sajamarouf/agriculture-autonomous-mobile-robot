# Raspberry Pi – AI Processing System

## Overview

The Raspberry Pi serves as the main AI processing unit of the agricultural robot. It uses computer vision and machine learning models to detect plants, classify fruit diseases, and communicate with the Arduino controller.

## Technologies Used

- Python
- OpenCV
- YOLO
- TensorFlow Lite (LiteRT)
- Picamera2
- FastAPI
- PySerial
- NumPy

## AI Models

The system uses two AI models:

**1. Plant Detection – YOLO**
- Detects plants in camera frames.
- Uses a confidence threshold of 0.50.
- Processes plant detection every 20 frames.

**2. Fruit Disease Classification – TensorFlow Lite**
- Classifies the detected plant condition.
- Uses a 224 × 224 input image.
- Uses a confidence threshold of 20%.

## Image Processing

- Captures images using Raspberry Pi Camera.
- Applies image zoom.
- Prepares images for model input.
- Processes images using the AI models.
- Displays detection and classification results.

## Arduino Communication

The Raspberry Pi communicates with Arduino through serial communication.

**Serial Configuration:**
- Port: `/dev/ttyACM0`
- Baud Rate: 9600

The system sends the following commands:

| Command | Purpose |
|---|---|
| `plant` | Stops the robot when a plant is detected. |
| `apple` | Sends the apple classification result. |
| `guava` | Sends the guava classification result. |
| `pomegranate` | Sends the pomegranate classification result. |

## FastAPI Endpoints

| Endpoint | Function |
|---|---|
| `/` | Checks whether the Raspberry Pi API is working. |
| `/result` | Returns the latest detection and classification results. |
| `/reset` | Resets the current detection state. |

## Detection Results

The API provides the following information:

- Ready status
- Detection lock status
- Plant type
- Fruit type
- Disease classification
- Confidence score
- Disease information

## System Workflow

1. Initialize the Raspberry Pi camera.
2. Capture camera frames.
3. Detect plants using YOLO.
4. Classify plant conditions using the TensorFlow Lite model.
5. Confirm the classification over time.
6. Stop the robot when a plant is detected.
7. Identify the fruit type.
8. Send the fruit type to Arduino.
9. Provide the latest results through FastAPI.

## Camera Controls

| Key | Function |
|---|---|
| `+` | Increase zoom. |
| `-` | Decrease zoom. |
| `r` | Reset detection state. |
| `q` | Exit the camera window. |

## Project File

`raspberry_pi_main.py` – Main Python program for camera processing, AI inference, Arduino communication, and API functionality.

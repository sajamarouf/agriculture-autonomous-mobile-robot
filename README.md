# Agriculture Autonomous Mobile Robot
### Graduation Project | Applied Science Private University | 2026

An intelligent mobile agricultural robot integrating robotics, Artificial Intelligence (AI), computer vision, and soil moisture sensing to monitor plant conditions and support smart irrigation decisions.

---

## 1. Project Overview

Efficient irrigation management and continuous plant health monitoring are essential for sustainable agriculture.

This project presents an autonomous mobile agricultural robot designed to move between plants, capture plant images, measure soil moisture, and analyze plant conditions using AI-based techniques.

The system combines a mobile robotic platform, image processing, soil moisture sensing, cloud-based data management, and a Flutter mobile application to support intelligent irrigation decisions.

## 2. Problem Statement

Traditional agricultural monitoring and irrigation practices often depend on manual inspection and conventional watering methods.

These approaches can make continuous plant monitoring difficult and may lead to inefficient water usage due to overwatering or underwatering.

The project addresses these challenges by integrating mobile robotics, computer vision, soil moisture sensing, and AI-based analysis into an agricultural monitoring and irrigation system.

## 3. Project Objectives

- Develop an autonomous mobile agricultural robot.
- Monitor plant health using computer vision.
- Measure soil moisture in real time.
- Support data-driven irrigation decisions.
- Improve water usage efficiency.
- Reduce manual intervention in agricultural monitoring.

## 4. System Architecture & Hardware

The system integrates the following hardware components:

| Component | Function |
|---|---|
| Raspberry Pi | Main processing unit |
| Arduino | Hardware and sensor control |
| RGB Camera | Plant image capture |
| Soil Moisture Sensor | Soil moisture measurement |
| Ultrasonic Sensors | Obstacle detection |
| DC Motors | Robot movement |
| Water Pump & Tank | Targeted irrigation |

**System Responsibilities**

- Raspberry Pi: Processes camera data, runs AI models, and communicates with other system components.
- Arduino: Reads sensor data and controls motors and the water pump.
- Mobile Application: Displays monitoring information, plant analysis, and irrigation records.

## 5. Technologies Used

### Artificial Intelligence & Computer Vision

| Technology | Application |
|---|---|
| YOLOv8 | Plant detection |
| MobileNetV2 | Fruit disease classification |
| TensorFlow / Keras | Deep learning model development |
| OpenCV | Image processing |
| Gemini | AI-based analysis and recommendations |
| ChatGPT | User-friendly explanations |

### Programming & Application Development

- Python
- Dart
- Flutter

### Cloud & Development Tools

- Firebase
- Google Colab
- Git
- GitHub
- Visual Studio Code

## 6. AI Models & Dataset

The project includes plant detection and fruit disease classification tasks.

### Plant Detection

YOLOv8 was evaluated for identifying plants in captured images, supporting the robot's plant monitoring workflow.

### Fruit Disease Classification

A MobileNetV2-based image classification model was implemented using TensorFlow and Keras.

**Model Configuration**

| Parameter | Value |
|---|---|
| Architecture | MobileNetV2 |
| Input Image Size | 224 × 224 |
| Number of Classes | 17 |
| Optimizer | Adam |
| Loss Function | Sparse Categorical Crossentropy |
| Training Epochs | Up to 20 |
| Batch Size | 32 |

**Dataset Information**

The project presentation describes a Kaggle dataset containing:

- 6,567 images
- Approximately 19 GB
- 4 fruit categories: Apple, Guava, Mango, and Pomegranate
- 17 classes representing healthy and diseased conditions

**Training Results**

The uploaded training notebook records the following test evaluation:

| Metric | Result |
|---|---:|
| Test Accuracy | 94.92% |
| Test Loss | 0.1629 |
| Test Images Evaluated | 984 |

*These results belong to the MobileNetV2 classification notebook, not the YOLOv8 plant detection model.*

## 7. System Methodology

The system combines the following operations:

1. The mobile robot moves between plants.
2. The camera captures plant images.
3. The computer vision pipeline processes captured images.
4. YOLOv8 supports plant detection.
5. AI models analyze plant conditions.
6. The soil moisture sensor collects soil readings.
7. The system uses plant and soil information to support irrigation decisions.
8. Arduino controls the motors and water pump according to received commands.
9. Data and results are communicated to Firebase and displayed through the mobile application.

## 8. Mobile Application

The Flutter mobile application provides an interface for monitoring and managing the agricultural system.

The documented application screens include:

- Welcome Screen
- Sign In
- Sign Up
- Dashboard
- Plants Repository
- Irrigation Log
- System Alerts

The application uses Firebase for cloud-based data storage and synchronization.

## 9. Project Gallery

### Robot Exhibition

![Robot Exhibition](robot-exhibition.png)

### Physical Robot Prototype

![Robot Prototype](robot-prototype.jpeg)

### Third Place Award

![Third Place Award](third-place-award.jpeg)

## 10. Project Demonstration

Watch the physical robot demonstration recorded during the university exhibition.

[▶ Watch Project Demonstration](robot-demonstration.mp4)

## 11. Achievement

**Third Place – ASU Expo FITers GP 2026**

The project received third place at the university graduation project exhibition.

## 12. Installation & Usage

The source code and project components are being organized for publication.

Detailed installation instructions, software dependencies, hardware connections, and execution commands will be documented alongside the corresponding source code.

## 13. Future Improvements

- Integrating solar energy as a renewable power source.
- Developing an automatic battery charging station.
- Developing an automatic water refilling station.
- Creating a Raspberry Pi-based mapping system for better monitoring and field management.
- Integrating fertilizer and nutrient sensors for precise plant nutrition management.

## 14. Conclusion

This project presents an intelligent agricultural monitoring and irrigation system that combines robotics, artificial intelligence, and computer vision.

By integrating mobile plant monitoring, soil moisture sensing, AI-based analysis, and automated irrigation, the system supports more efficient water management and data-driven agricultural practices.

---

## Project Source Code

### Arduino
[Arduino Code and Documentation](Arduino/)

### Raspberry Pi
[Raspberry Pi Code and Documentation](Raspberry-Pi/)

### Mobile Application
[Flutter Application and Documentation](Mobile-App/)

### AI Model Training
[Fruit Disease Classification Notebook](fruit_disease_classification.ipynb)

## Project Media

- [Robot Demonstration Video](robot-demonstration.mp4)
- [Robot Exhibition](robot-exhibition.png)
- [Physical Robot Prototype](robot-prototype.jpeg)
- [Third Place Award](third-place-award.jpeg)

---

**Agriculture Autonomous Mobile Robot**

Applied Science Private University | Faculty of Information Technology | 2026

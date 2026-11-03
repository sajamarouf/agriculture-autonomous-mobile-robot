# Fruit Disease Classification Using Deep Learning

## Project Overview
An AI-based image classification project designed to identify fruit diseases using deep learning and transfer learning techniques.

The model classifies images of four fruit types (Apple, Mango, Guava, and Pomegranate) into 17 healthy and disease categories.

## Dataset
- Total Images: 6,537
- Number of Classes: 17
- Fruit Categories: 4
- Image Dimensions: 224 × 224 pixels
- Training Set: 4,571 images (70%)
- Validation Set: 982 images (15%)
- Testing Set: 984 images (15%)

## Technologies & Tools
- Python
- TensorFlow & Keras
- MobileNetV2
- OpenCV
- rembg
- Google Colab (GPU)
- TensorFlow Lite

## Methodology

### 1. Image Preprocessing
- Removed image backgrounds using rembg.
- Replaced backgrounds with black backgrounds.
- Resized images to 224 × 224 pixels.
- Organized images into 17 classification categories.

### 2. Dataset Preparation
Split the dataset into:
- 70% Training
- 15% Validation
- 15% Testing

### 3. Model Architecture
Used MobileNetV2 with ImageNet pretrained weights through Transfer Learning.

The classification architecture includes:
- MobileNetV2 as a frozen feature extractor.
- Global Average Pooling.
- Dense layer with 128 neurons and ReLU activation.
- Dropout layer (0.3).
- Softmax output layer with 17 classes.

### 4. Model Training
- Optimizer: Adam
- Loss Function: Sparse Categorical Crossentropy
- Batch Size: 32
- Maximum Epochs: 20
- Early Stopping: Enabled (patience = 3)
- Input Image Size: 224 × 224

## Model Performance

| Evaluation Metric | Result |
|---|---:|
| Validation Accuracy | 95.62% |
| Test Accuracy | 94.92% |
| Test Loss | 0.1629 |

The model achieved approximately 94.92% accuracy on the held-out test dataset.

## Model Export
The trained model was exported in two formats:

- `Newfruit_disease_model_final.h5`
- `Newfruit_disease_model_final.tflite`

Class labels were saved in:
- `Newclasses.txt`

TensorFlow Lite conversion was performed to support potential deployment on mobile and edge devices.

## Key Learning Outcomes
- Applied Transfer Learning using MobileNetV2.
- Performed image preprocessing and background removal.
- Prepared and organized a multi-class image dataset.
- Trained and evaluated a deep learning classification model.
- Converted a trained TensorFlow model into TensorFlow Lite format.

## Project Status
Completed — Model training, evaluation, and export.

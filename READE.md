#  Helmet Detection and Tracking System
#  安全帽自動偵測與追蹤系統

🌍 *[English](#english-version) | [繁體中文](#繁體中文版本)*

---

<a id="english-version"></a>
## 🇬🇧 English Version

This is an End-to-End AI computer vision project built with **YOLO26s** and **Streamlit**. The system performs real-time motorcycle helmet detection on footage from intersection traffic cameras or dashcams, and integrates tracking algorithms to automatically capture screenshots of violations.

### ✨ Features

* 📷 **Multi-Source Video Support**: Supports uploading images, MP4 videos, and **real-time YouTube livestream analysis** (e.g., directly inputting the URL of a live traffic camera in Beitun District, Taichung, or other locations for monitoring).
* 🎯 **Smart Object Tracking (ByteTrack)**: Built-in tracking algorithms assign a unique ID to each target, ensuring the same violator is **not ticketed multiple times**, significantly reducing false positives and alert spam.
* 🚨 **Automated Violation Alerts**: When a rider without a helmet is detected, the system's sidebar triggers a real-time alert and automatically captures a screenshot of the violation as evidence.
* 🐳 **Docker Containerization**: One-click environment setup that perfectly resolves dependency and conflict issues. Fully supports NVIDIA GPU acceleration.

### 🛠️ Tech Stack

* **AI Model**: YOLO26s (Ultralytics)
* **Frontend & Dashboard**: Streamlit
* **Image Processing**: OpenCV
* **Containerization**: Docker & Docker Compose
* **Hardware Acceleration**: NVIDIA CUDA / TensorRT Deployment Supported

### 🚀 Quick Start

#### 1. Environment Setup
Please ensure Docker, Docker Compose, and NVIDIA GPU drivers are installed on your machine.

#### 2. Download Model Weights
> **⚠️ Note:** Due to GitHub's file size limits, the model weights are not included in this repository. 
> Please download the trained `best.pt` from [Insert your Google Drive link here] and place it in the `/workspace/runs/weights/` directory (or modify the model path in `web.py`).

#### 3. Start Services
Open a terminal in the project root directory and run the following commands:
```bash
# Build and start the Docker container
docker compose up -d --build

# Start the Streamlit web server
docker compose exec yolo streamlit run app/web.py --server.address 0.0.0.0 --server.port 8501
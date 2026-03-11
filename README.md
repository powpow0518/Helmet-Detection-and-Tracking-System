# Helmet Detection and Tracking System
# 安全帽偵測與追蹤系統

🌍 [English](#english-version) | [繁體中文](#繁體中文版本)

---

<a id="english-version"></a>
## English Version

This project is a simple computer vision application built with **YOLO26s** and **Streamlit**.  
It detects whether motorcycle riders are wearing helmets from videos or images. The system can process footage from intersection cameras or dashcams and capture screenshots when a rider without a helmet is detected.

The goal of this project is to demonstrate how an object detection model can be integrated into a small web application for real-time analysis.

### Features

**Multiple input sources**

The system supports images, MP4 videos, and YouTube livestream URLs. This allows it to analyze traffic camera streams or uploaded videos.

**Object tracking**

ByteTrack is used to assign an ID to each detected rider. This helps avoid capturing the same person repeatedly across frames.

**Violation screenshot**

When a rider without a helmet is detected, the system automatically saves a screenshot and shows the alert in the sidebar.

**Docker deployment**

The environment can be started using Docker and Docker Compose, which helps keep dependencies consistent. GPU acceleration with NVIDIA CUDA is supported if available.

### Tech Stack

- YOLO26s (Ultralytics)
- Streamlit
- OpenCV
- Docker / Docker Compose
- NVIDIA CUDA (optional)

### Quick Start

#### 1. Requirements

Make sure the following tools are installed:

- Docker
- Docker Compose
- NVIDIA GPU Driver (optional, for GPU acceleration)

#### 2. Download Model Weights

Due to GitHub file size limits, the trained model weights are not included in this repository.

Please download the `best.pt` file from your storage link (for example Google Drive) and place it in:

`/workspace/runs/weights/`

You can also modify the model path in `webcam.py` if needed.

#### 3. Start the Application

From the project root directory, run:

```bash
docker compose up -d --build
docker compose exec yolo streamlit run app/webcam.py --server.address 0.0.0.0 --server.port 8501
```

After the service starts, open your browser and go to:

http://localhost:8501

You should then see the Streamlit interface where videos or images can be uploaded for detection.

<a id="繁體中文版本"></a>
## 🇹🇼 繁體中文版本

這是一個使用 **YOLO26s** 與 **Streamlit** 開發的電腦視覺專案，主要用來偵測機車騎士是否配戴安全帽。系統可以分析路口監視器或行車紀錄器的影片，並在偵測到未戴安全帽時自動截圖與標記。

### 功能

* **多來源影片支援**  
  支援圖片、MP4 影片，以及 YouTube 即時直播串流（例如交通監視器直播）。

* **物件追蹤（ByteTrack）**  
  系統會替每個偵測到的目標分配 ID，避免同一個人被重複判定。

* **違規畫面截圖**  
  偵測到未配戴安全帽時會自動截圖並顯示在側邊欄。

* **Docker 部署**  
  使用 Docker 與 Docker Compose 建立執行環境，並支援 NVIDIA GPU。

### 使用技術

* YOLO26s (Ultralytics)
* Streamlit
* OpenCV
* Docker / Docker Compose
* NVIDIA CUDA

### 快速開始

#### 1. 環境準備
請先安裝：

- Docker
- Docker Compose
- NVIDIA GPU Driver（若要使用 GPU）

#### 2. 下載模型權重

由於 GitHub 有檔案大小限制，本專案沒有包含模型權重。

請下載 `best.pt` 並放到：

`/workspace/runs/weights/`

或自行修改 `webcam.py` 的模型路徑。

#### 3. 啟動服務

在專案根目錄執行：

```bash
docker compose up -d --build
docker compose exec yolo streamlit run app/webcam.py --server.address 0.0.0.0 --server.port 8501
```

啟動後可在瀏覽器開啟：

http://localhost:8501
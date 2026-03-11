PROJECT_DIR = "/workspace/runs"
BASE_NAME = "yolo26s"
STAGE1_NAME = f"{BASE_NAME}_stage1"
MODEL_NAME = "yolo26s"

TRAIN_ARGS = {
    "epochs": 200,
    "patience": 20,
    "imgsz": 640,
    "batch": 6,
    "workers": 3,

    "optimizer": "AdamW",
    "lr0": 0.001,

    "freeze": None,

    "degrees": None,
    "hsv_h": None,
    "hsv_s": None,
    "hsv_v": None

}

FINETUNE_ARGS = {
    "epochs": 10,
    "imgsz": 640,
    "batch": 6,
    "device": 0,
    "workers": 3,

    "optimizer": "AdamW",
    "lr0": 0.001,

    "mosaic": 0.0,         
    "close_mosaic": 0,     
    "degrees": 0.0,        
    "mixup": 0.0
}
import os
from ultralytics import YOLO
from config import PROJECT_DIR, STAGE1_NAME, BASE_NAME, FINETUNE_ARGS


def evaluate_on_test_set():
    print("正在載入訓練好的最佳模型...")
    
    best_model_path = os.path.join(PROJECT_DIR, STAGE1_NAME, "weights", "best.pt")
    model = YOLO(best_model_path)
    
    print("開始使用 test (測試集) 評估模型效能...")
    
    model.train(
        data="/workspace/data/helmet_yolo/dataset.yaml",            
        project=PROJECT_DIR, 
        name=BASE_NAME, 
        **FINETUNE_ARGS
    )

    metrics = model.val(
        data="/workspace/data/helmet_yolo/dataset.yaml",
        split="test", 
        device=0 
    )
    
    print("\n==================================")
    print(f"✅ mAP50 : {metrics.box.map50:.4f}")
    print(f"✅ mAP50-95 : {metrics.box.map:.4f}")
    print("==================================")

if __name__ == "__main__":
    evaluate_on_test_set()
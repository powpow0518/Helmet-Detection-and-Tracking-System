import os
import shutil
from ultralytics import YOLO
from config import PROJECT_DIR, BASE_NAME, TRAIN_ARGS, STAGE1_NAME, FINETUNE_ARGS, MODEL_NAME

def train_model():
    print("載入 YOLO26 預訓練模型...")
    # 載入我們之前下載好的模型當作基礎
    model = YOLO(f"{MODEL_NAME}.pt")
    active_args = {k: v for k, v in TRAIN_ARGS.items() if v is not None}    
    print("開始第一階段訓練...")
    
    # 執行訓練
    model.train(
        data="/workspace/data/helmet_yolo/dataset.yaml", 
        project=PROJECT_DIR, 
        name=STAGE1_NAME,   
        **active_args 
    )
    
    print("\n 第一階段訓練結束！")
    print("第二階段訓練開始...\n")

    best_model_path = os.path.join(PROJECT_DIR, STAGE1_NAME, "weights", "best.pt")

    model_finetune = YOLO(best_model_path)

    model_finetune.train(
        data="/workspace/data/helmet_yolo/dataset.yaml",            
        project=PROJECT_DIR, 
        name=BASE_NAME, 
        **FINETUNE_ARGS
    )

    print("\n 第二階段訓練結束！")
    print("\n 開始測試 test 效能...")

    metrics = model_finetune.val(
        data="/workspace/data/helmet_yolo/dataset.yaml",
        split="test", 
        device=0 
    )

    map50 = metrics.box.map50
    map50_95 = metrics.box.map

    print("\n==================================")
    print(f"✅ mAP50 : {map50:.4f}")
    print(f"✅ mAP50-95 : {map50_95:.4f}")
    print("==================================")

    log_file = "scores.txt"
    
    headers = ["base_name", "mAP50", "mAP50-95"] + list(TRAIN_ARGS.keys())
    values = [BASE_NAME, f"{map50:.4f}", f"{map50_95:.4f}"] + [str(v) for v in TRAIN_ARGS.values()]
    
    header_str = "\t".join(headers)
    value_str = "\t".join(values)
    
    # 如果檔案不存在，先寫入標題列
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write(header_str + "\n")
        f.write(value_str + "\n")
        
    print(f"實驗紀錄已成功儲存至 {log_file}！")

    stage1_path = os.path.join(PROJECT_DIR, STAGE1_NAME)
    if os.path.exists(stage1_path):
        print(f"\n 正在刪除過渡資料夾 {STAGE1_NAME} ...")
        shutil.rmtree(stage1_path)
        print("✨ 清理完成！")


if __name__ == "__main__":
    train_model()
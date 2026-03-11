import torch
from ultralytics import YOLO

def test_environment():
    print("=== 系統環境檢查 ===")
    # 檢查有沒有抓到你的 RTX 2060
    cuda_available = torch.cuda.is_available()
    print(f"GPU 可用狀態: {cuda_available}")
    
    if cuda_available:
        print(f"顯卡名稱: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ 警告：沒有抓到 GPU，目前只能用 CPU 運算。")
    
    print("\n=== YOLOv8 模型測試 ===")
    # 第一次執行時，這行會自動下載 yolov8n.pt
    model = YOLO("app/models/yolov8n.pt") 
    
    # 拿官方的一張街景公車圖來做測試
    print("開始進行物件偵測...")
    results = model("https://ultralytics.com/images/bus.jpg")
    
    print("\n🎉 測試完成！YOLOv8 成功運作！")

if __name__ == "__main__":
    test_environment()
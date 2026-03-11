import cv2
from ultralytics import YOLO

def process_video():
    print("🎬 正在載入模型...")
    model = YOLO("/workspace/runs/yolo26s/weights/best.pt")
    
    input_folder = "/workspace/data/test_video"
        
    results = model.predict(
        source=input_folder,
        save=True,
        project="/workspace/data",
        name="result_video",
        exist_ok=True,
        conf=0.35,
        stream=True
    )
    
    # 讓 generator 執行完畢 
    for r in results:
        pass
        
    print("\n 影片辨識完成！")

if __name__ == "__main__":
    process_video()
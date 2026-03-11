import os
import shutil

def merge_hard_samples():
    print("將「錯題本」併入主力訓練集...")
    
    # 📍 來源資料夾 (你剛剛用 labelImg 標註存檔的地方)
    source_dir = "/workspace/data/cut"
    
    # 🎯 目的地資料夾 (YOLO 的嚴格規定：圖片跟標籤必須分開)
    target_images_dir = "/workspace/data/helmet_yolo/images/train"
    target_labels_dir = "/workspace/data/helmet_yolo/labels/train"
    
    # 防呆機制：如果來源資料夾不存在，先擋下來
    if not os.path.exists(source_dir):
        print(f"❌ 找不到來源資料夾：{source_dir}，請確認名稱是否正確！")
        return

    # 確保目的地資料夾存在
    os.makedirs(target_images_dir, exist_ok=True)
    os.makedirs(target_labels_dir, exist_ok=True)
    
    # 支援的圖片副檔名
    valid_image_exts = ['.jpg', '.jpeg', '.png']
    
    image_count = 0
    label_count = 0
    
    for filename in os.listdir(source_dir):
        # ⚠️ 絕對不要把 classes.txt 搬進去，會害 YOLO 報錯！
        if filename == "classes.txt":
            continue
            
        file_path = os.path.join(source_dir, filename)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        # 📦 分發邏輯：圖片走左邊，標籤走右邊
        # 這裡用 shutil.copy (複製)，保留 hard_samples 裡的檔案當作你的備份
        if ext in valid_image_exts:
            shutil.copy(file_path, os.path.join(target_images_dir, filename))
            image_count += 1
        elif ext == '.txt':
            shutil.copy(file_path, os.path.join(target_labels_dir, filename))
            label_count += 1
            
    print("\n==================================================")
    print(f"搬運完成！")
    print(f"複製了 {image_count} 張圖片到 images/train")
    print(f"複製了 {label_count} 個標籤到 labels/train")
    print("==================================================")


if __name__ == "__main__":
    merge_hard_samples()
import os
import glob
import xml.etree.ElementTree as ET
import random
import shutil

# 設定路徑
DATA_ROOT = "/workspace/data/helmet-detection"
XML_DIR = os.path.join(DATA_ROOT, "annotations")
IMG_DIR = os.path.join(DATA_ROOT, "images")
OUTPUT_DIR = "/workspace/data/helmet_yolo"

# 🌟 明確指定要抓取的標籤名稱 (大小寫與空格必須與 XML 內完全一致)
CLASSES = ["With Helmet", "Without Helmet"]

def convert_box(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)

def setup_directories():
    # 如果舊資料夾存在，先清空它 (連同壞掉的 .cache 檔一起刪除)
    if os.path.exists(OUTPUT_DIR):
        print("🧹 發現舊的資料夾，正在清空重置...")
        shutil.rmtree(OUTPUT_DIR)
        
    print("📁 正在建立 YOLO 格式的 Train/Val/Test 資料夾結構...")
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(OUTPUT_DIR, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(OUTPUT_DIR, 'labels', split), exist_ok=True)

def process_data():
    setup_directories()
    
    xml_files = glob.glob(os.path.join(XML_DIR, "*.xml"))
    random.seed(42)
    random.shuffle(xml_files)
    
    total_files = len(xml_files)
    train_idx = int(total_files * 0.7)
    val_idx = int(total_files * 0.9) 
    
    print(f"⏳ 開始轉換標註檔並搬移圖片 (總計 {total_files} 筆)...")
    print(f"📊 分配比例：Train={train_idx}筆, Val={val_idx-train_idx}筆, Test={total_files-val_idx}筆")
    
    for idx, xml_file in enumerate(xml_files):
        if idx < train_idx:
            split = 'train'
        elif idx < val_idx:
            split = 'val'
        else:
            split = 'test'
            
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        img_name = root.find('filename').text
        base_name = os.path.splitext(os.path.basename(xml_file))[0]
        img_path = os.path.join(IMG_DIR, base_name + ".png") 
        
        if not os.path.exists(img_path):
            continue
            
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        
        txt_name = base_name + ".txt"
        txt_path = os.path.join(OUTPUT_DIR, 'labels', split, txt_name)
        
        with open(txt_path, 'w') as out_file:
            for obj in root.iter('object'):
                cls_name = obj.find('name').text
                
                # 嚴格比對 CLASSES 清單，對不上的直接跳過
                if cls_name not in CLASSES:
                    continue
                cls_id = CLASSES.index(cls_name)
                
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
                     float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert_box((w, h), b)
                out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")
                
        shutil.copy(img_path, os.path.join(OUTPUT_DIR, 'images', split, img_name))

    print("✅ 資料轉換完成！")

    # 更新 dataset.yaml 配合新的類別名稱
    yaml_content = f"""
path: /workspace/data/helmet_yolo
train: images/train
val: images/val
test: images/test

names:
  0: With Helmet
  1: Without Helmet
"""
    with open(os.path.join(OUTPUT_DIR, "dataset.yaml"), "w") as f:
        f.write(yaml_content.strip())
    print("📝 dataset.yaml 設定檔已建立完成！")

if __name__ == "__main__":
    process_data()
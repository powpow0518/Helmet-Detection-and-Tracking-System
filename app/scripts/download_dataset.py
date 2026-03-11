import os
import subprocess

def download_helmet_dataset():
    print("⏳ 開始透過 Kaggle 官方 CLI 下載安全帽資料集...")
    
    # 這是我們要把圖片存放的最終位子
    dest_path = "/workspace/data/helmet-detection"
    os.makedirs(dest_path, exist_ok=True)
    
    # 組合 Kaggle CLI 指令
    # 等同於在終端機打: kaggle datasets download -d andrewmvd/helmet-detection -p /workspace/data/helmet-detection --unzip
    command = [
        "kaggle", "datasets", "download", 
        "-d", "andrewmvd/helmet-detection", 
        "-p", dest_path, 
        "--unzip"
    ]
    
    try:
        # 直接呼叫系統指令執行下載
        subprocess.run(command, check=True)
        print(f"\n🎉 大功告成！資料集已成功下載並解壓縮至: {dest_path}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 下載失敗，請檢查 .env 裡面的 KAGGLE_API_TOKEN 是否正確！")
        print(f"錯誤代碼: {e}")

if __name__ == "__main__":
    # 確保你有把 Token 讀進來，印出來檢查一下 (基於安全，只印出前5個字元)
    token = os.environ.get("KAGGLE_API_TOKEN", "")
    if token:
        print(f"✅ 成功讀取 KAGGLE_API_TOKEN (開頭為 {token[:5]}...)")
    else:
        print("⚠️ 警告：沒有讀取到 KAGGLE_API_TOKEN 環境變數！")
        
    download_helmet_dataset()
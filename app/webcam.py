import os
import streamlit as st
import cv2
import tempfile
from ultralytics import YOLO

# 🌟 1. 網頁基本設定
st.set_page_config(page_title="安全帽偵測系統", page_icon="👮‍♂️", layout="wide")
st.title("安全帽自動偵測系統")
st.markdown("上傳路口監視器影片或圖片，AI 將為您即時抓出未戴安全帽的違規者！")

# 🌟 2. 側邊欄：控制台
st.sidebar.header("⚙️ 控制台")
# 讓使用者可以在網頁上自己拖拉設定信心指數！
conf_threshold = st.sidebar.slider("閥值 (Confidence)", min_value=0.1, max_value=1.0, value=0.5, step=0.05)

# 載入你剛才認可的冠軍模型！(請換成你最終版的 best.pt 路徑)
@st.cache_resource # 快取模型，避免每次上傳都重新載入
def load_model():
    return YOLO("/workspace/runs/yolo26s/weights/best.pt")

model = load_model()
st.sidebar.success("✅ AI 載入完成！")

st.sidebar.markdown("---")
st.sidebar.header("🚨 違規區")
# 挖兩個空位，一個放警告文字，一個放最新違規截圖
alert_text = st.sidebar.empty()  
alert_image = st.sidebar.empty()

# 🌟 3. 主畫面：檔案上傳區
source_type = st.radio("📡 選擇影像來源", ["📂 上傳檔案 (圖片/影片)", "🔴 YouTube 即時直播"])

if source_type == "📂 上傳檔案 (圖片/影片)":
    uploaded_file = st.file_uploader("請上傳測試圖片或影片 (.jpg, .png, .mp4)", type=['jpg', 'jpeg', 'png', 'mp4'])
    
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        
        # 📷 [圖片處理區塊] 
        if file_ext in ['jpg', 'jpeg', 'png']:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📷 原始圖片")
                st.image(uploaded_file, width="stretch")
            with col2:
                st.subheader("🎯 AI 辨識結果")
                with st.spinner("AI 正在鷹眼掃描中..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    results = model.predict(source=tmp_path, conf=conf_threshold)
                    res_plotted = results[0].plot()
                    res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                    st.image(res_rgb, width="stretch")
                    
                    classes_detected = results[0].boxes.cls.cpu().numpy()
                    if 1 in classes_detected:
                        alert_text.error("⚠️ 警告：發現未戴安全帽違規！")
                        alert_image.image(res_rgb, width="stretch", caption="📸 違規證據截圖")
                    else:
                        alert_text.success("✅ 畫面中無違規情事。")
                    os.remove(tmp_path) 
                    
        # 🎬 [影片處理區塊]
        elif file_ext == 'mp4':
            st.subheader("🎬 AI 影片即時辨識與追蹤中...")
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_video_path = tmp_file.name
                
            cap = cv2.VideoCapture(tmp_video_path)
            stframe = st.empty()
            violation_count = 0 
            fined_ids = set()   
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                    
                results = model.track(source=frame, conf=conf_threshold, persist=True, verbose=False)
                annotated_frame = results[0].plot()
                stframe.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB), channels="RGB", width="stretch")
                
                boxes = results[0].boxes
                if boxes is not None and boxes.id is not None:
                    for cls, track_id in zip(boxes.cls.cpu().numpy(), boxes.id.cpu().numpy()):
                        if int(cls) == 1 and track_id not in fined_ids:
                            fined_ids.add(track_id)
                            violation_count += 1
                            alert_text.error(f"⚠️ 科技執法舉發！\n已累計開出 {violation_count} 張罰單")
                            alert_image.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB), channels="RGB", width="stretch", caption=f"📸 最新違規證據 (#{int(track_id)})")
            cap.release()
            os.remove(tmp_video_path)

# ==========================================
# 🔴 YouTube 直播處理區塊 (全新功能！)
# ==========================================
elif source_type == "🔴 YouTube 即時直播":
    st.subheader("🔴 連結 YouTube 路口監視器直播")
    st.info("💡 請將outube網址貼在下方。")
    youtube_url = st.text_input("貼上 YouTube 直播網址：", value="")
    
    # 這裡用 Checkbox 當作「開始/停止」的按鈕，這是 Streamlit 處理無限迴圈最棒的寫法！
    is_running = st.checkbox("開始偵測 👮‍♂️")
    
    if is_running and youtube_url:
        stframe = st.empty()
        violation_count = 0 
        fined_ids = set()   
        
        try:
            # 🌟 神奇魔法：YOLO 加上 stream=True，就可以像水管一樣源源不絕地接收直播畫面！
            results = model.track(source=youtube_url, stream=True, conf=conf_threshold, persist=True, verbose=False)
            
            for r in results:
                # 取得當下這 1 幀畫面
                annotated_frame = r.plot()
                annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                stframe.image(annotated_frame_rgb, channels="RGB", width="stretch")
                
                # 🕵️‍♂️ 一樣套用不重複開單的黑名單邏輯
                boxes = r.boxes
                if boxes is not None and boxes.id is not None:
                    classes_detected = boxes.cls.cpu().numpy() 
                    track_ids = boxes.id.cpu().numpy()         
                    
                    for cls, track_id in zip(classes_detected, track_ids):
                        if int(cls) == 1:
                            if track_id not in fined_ids:
                                fined_ids.add(track_id)
                                violation_count += 1
                                alert_text.error(f"⚠️ 科技執法舉發！\n直播中已累計開出 {violation_count} 張罰單")
                                alert_image.image(
                                    annotated_frame_rgb, 
                                    channels="RGB", 
                                    width="stretch", 
                                    caption=f"📸 即時違規證據 (追蹤編號: #{int(track_id)})"
                                )
                                
        except Exception as e:
            st.error(f"❌ 讀取直播失敗，請確認該網址是公開的 YouTube 直播。\n錯誤訊息: {e}")
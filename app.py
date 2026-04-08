import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="地震速報 AI 助手 (Hackathon)", layout="centered")
st.title("🌋 地震速報 AI 產稿助手")

# 1. 取得 API Key
API_KEY = st.secrets.get("api_key")

if not API_KEY:
    st.error("❌ 找不到 API Key，請檢查 Streamlit Secrets 設定。")
    st.stop()

# 2. 自動列出所有可用模型 (關鍵步驟)
try:
    genai.configure(api_key=API_KEY)
    # 抓取支援產出內容的模型
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    with st.sidebar:
        st.success("✅ API 連線成功")
        st.write("您的帳號可用模型：")
        st.code(available_models)
        
    # 自動選擇清單中的第一個 Flash 模型，如果沒有就選第一個
    target_model = next((m for m in available_models if "flash" in m), available_models[0])
    st.info(f"系統已自動切換至最佳模型：`{target_model}`")

except Exception as e:
    st.error(f"🚨 API Key 驗證失敗：{e}")
    st.stop()

# 3. 圖片上傳與處理
uploaded_file = st.file_uploader("上傳地震速報圖卡", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("🚀 產出主播稿"):
        try:
            model = genai.GenerativeModel(target_model)
            prompt = "你是一位專業新聞主播，請根據這張地震圖卡，撰寫一段主播稿與一個新聞標題。"
            
            with st.spinner('AI 正在分析圖片數據...'):
                response = model.generate_content([prompt, image])
                st.success("產出成功！")
                st.markdown("---")
                st.write(response.text)
        except Exception as e:
            st.error(f"產出失敗：{e}")

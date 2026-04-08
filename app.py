import streamlit as st
import google.generativeai as genai
from PIL import Image

# 讀取 Secrets
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    API_KEY = None

st.set_page_config(page_title="地震速報 AI 播報助手", layout="centered")
st.title("🌋 地震速報 AI 播報助手")

# --- 側邊欄：診斷工具 ---
with st.sidebar:
    st.header("🛠️ 系統診斷")
    if API_KEY:
        if st.button("查看我可用的 AI 模型"):
            try:
                genai.configure(api_key=API_KEY)
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                st.write(models)
            except Exception as e:
                st.error(f"無法取得清單：{e}")
    else:
        API_KEY = st.text_input("輸入 API Key", type="password")

# --- 主程式 ---
uploaded_file = st.file_uploader("上傳地震圖卡", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("🚀 產出文稿"):
        if not API_KEY:
            st.error("請提供 API Key")
        else:
            try:
                genai.configure(api_key=API_KEY)
                
                # 【關鍵優化】：嘗試多個可能的模型名稱，直到成功為止
                model_names = ['gemini-3-flash', 'gemini-1.5-flash', 'gemini-pro-vision']
                success = False
                
                for m_name in model_names:
                    try:
                        model = genai.GenerativeModel(m_name)
                        # 測試一下模型是否可用
                        prompt = "請根據這張地震圖卡，產出主播稿與標題。"
                        response = model.generate_content([prompt, image])
                        st.success(f"使用模型：{m_name}")
                        st.markdown("---")
                        st.markdown(response.text)
                        success = True
                        break # 成功了就跳出迴圈
                    except:
                        continue # 失敗就試下一個
                
                if not success:
                    st.error("目前所有 AI 模型都無法回應，請檢查 API Key 是否有權限或稍後再試。")
                    
            except Exception as e:
                st.error(f"系統錯誤：{e}")

import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. 頁面基礎設定 ---
st.set_page_config(page_title="地震速報 AI 助手", page_icon="🌋")

st.title("🌋 地震速報 AI 播報助手")
st.write("上傳圖卡，自動產出專業主播文稿。")

# --- 2. 取得 API Key ---
API_KEY = st.secrets.get("api_key")

if not API_KEY:
    with st.sidebar:
        API_KEY = st.text_input("請輸入 Gemini API Key", type="password")

# --- 3. 定義快取函式 (修正語法錯誤版本) ---
@st.cache_data(show_spinner=False)
def get_ai_response(api_key, model_name, image_bytes):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    img = Image.open(io.BytesIO(image_bytes))
    
    # 確保這裡的引號有開有寫
    prompt = "你是一位專業新聞主播。請根據這張地震圖卡，產出一份包含【新聞標題】與【主播文稿】的內容。標題格式：[時間][地點]規模[數字]地震。文稿請參考氣象署格式，確保各地震度準確。"
    
    response = model.generate_content([prompt, img])
    return response.text

# --- 4. 執行介面 ---
uploaded_file = st.file_uploader("上傳地震圖卡", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    st.image(Image.open(io.BytesIO(file_bytes)), use_container_width=True)
    
    if st.button("🚀 產出主播文稿"):
        if not API_KEY:
            st.error("請提供 API Key")
        else:
            try:
                with st.spinner('AI 編稿中...'):
                    # 如果 gemini-2.5-flash 還是不行，可以改成 gemini-1.5-flash
                    result = get_ai_response(API_KEY, "gemini-1.5-flash", file_bytes)
                    st.success("產出成功！")
                    st.markdown("---")
                    st.markdown(result)
            except Exception as e:
                st.error(f"錯誤：{e}")
                if "429" in str(e):
                    st.warning("提醒：流量超限，請等 30 秒再試。")

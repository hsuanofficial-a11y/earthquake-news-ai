import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="地震速報 AI 播報助手",
    page_icon="🌋",
    layout="centered"
)

# 套用一點簡單的自定義 CSS 增加專業感
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌋 地震速報 AI 播報助手")
st.write("上傳氣象署圖卡，自動產出專業主播文稿與標題。")

# --- 2. 取得 API Key (優先從 Secrets 讀取) ---
API_KEY = st.secrets.get("api_key")

if not API_KEY:
    with st.sidebar:
        st.warning("🔑 尚未偵測到 API Key")
        API_KEY = st.text_input("請輸入 Gemini API Key", type="password")
        st.caption("取得 Key: [Google AI Studio](https://aistudio.google.com/)")

# --- 3. 定義快取函式 (這能幫你省下大量額度！) ---
@st.cache_data(show_spinner=False)
def get_ai_response(api_key, model_name, image_bytes):
    """
    使用快取確保同一張圖片不會重複呼叫 API 扣額度。
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    # 將 bytes 轉回 PIL Image 供 AI 讀取
    img = Image.open(io.BytesIO(image_bytes))
    
    prompt = """
    你是一位專業的新聞台編稿人員。請精確讀取地震速報圖卡內容，並按照以下格式產出：
    
    【新聞主播文稿】
    最新消息，根據氣象署最新資訊，今天[日期]稍早[時間]發生芮氏規模

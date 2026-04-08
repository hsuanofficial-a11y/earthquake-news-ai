import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. 基礎設定 ---
st.set_page_config(page_title="地震速報 AI 助手", page_icon="🌋")
st.title("🌋 地震速報 AI 播報助手")

# --- 2. 取得 API Key ---
API_KEY = st.secrets.get("api_key")
if not API_KEY:
    with st.sidebar:
        API_KEY = st.text_input("請輸入 API Key", type="password")

# --- 3. 自動偵測模型的快取函式 ---
@st.cache_data(show_spinner=False)
def get_ai_response(api_key, image_bytes):
    genai.configure(api_key=api_key)
    
    # 【關鍵：自動找模型】不寫死名稱，直接從清單抓第一個可用的 Flash 模型
    model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # 優先選 2.5，沒 2.5 選 Flash，再沒辦法就選第一個
    target = next((m for m in model_list if "2.5-flash" in m), 
                 next((m for m in model_list if "flash" in m), model_list[0]))
    
    model = genai.GenerativeModel(target)
    img = Image.open(io.BytesIO(image_bytes))
    
    prompt = "你是一位專業新聞主播。請根據這張地震圖卡，產出一份包含【新聞標題】與【主播文稿】的內容。標題格式：[時間][地點]規模[數字]地震。文稿請參考氣象署格式，確保各地震度準確。"
    
    response = model.generate_content([prompt, img])
    return response.text, target

# --- 4. 介面操作 ---
uploaded_file = st.file_uploader("上傳地震圖卡", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    st.image(Image.open(io.BytesIO(file_bytes)), use_container_width=True)
    
    if st.button("🚀 產出主播文稿"):
        if not API_KEY:
            st.error("請提供 API Key")
        else:
            try:
                with st.spinner('AI 正在尋找可用模型並編稿中...'):
                    # 呼叫自動偵測函式
                    result_text, used_model = get_ai_response(API_KEY, file_bytes)
                    
                    st.success(f"產出成功！(使用模型: {used_model})")
                    st.markdown("---")
                    st.markdown(result_text)
            except Exception as e:
                # 處理 429 額度超限
                if "429" in str(e):
                    st.error("🚨 流量超限！免費版每分鐘限 5 次。")
                    st.warning("請現場等候 20 秒，讓冷卻時間過去再試。")
                else:
                    st.error(f"連線錯誤：{e}")
                    st.info("請確認 API Key 是否正確。")

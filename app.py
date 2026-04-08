import streamlit as st
import google.generativeai as genai
from PIL import Image

# 自動從 Streamlit Secrets 讀取 API Key
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    API_KEY = None

st.set_page_config(page_title="地震速報 AI 播報助手", layout="centered")

st.title("🌋 地震速報 AI 播報助手")
st.write("上傳氣象署地震圖卡，立即產出專業主播文稿。")

if not API_KEY:
    with st.sidebar:
        st.warning("⚠️ 尚未偵測到 API Key")
        API_KEY = st.text_input("請手動輸入 Gemini API Key", type="password")

uploaded_file = st.file_uploader("請上傳地震速報圖卡 (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="待處理圖卡", use_container_width=True)
    
    if st.button("🚀 產出文稿與標題"):
        if not API_KEY:
            st.error("請提供 API Key 才能開始作業喔！")
        else:
            try:
                genai.configure(api_key=API_KEY)
                # 這裡改成了最新的 gemini-3-flash
                model = genai.GenerativeModel('gemini-3-flash')

                prompt = """
                你是一位專業的新聞編稿人員。請精確讀取這張地震速報圖卡上的文字與數據，並產出以下內容：
                
                1. 【新聞標題】：格式為「[發生時間][震央地點]規模[數字]地震 最大震度[數字]級」
                2. 【主播文稿】：以「最新消息，根據氣象署最新資訊...」開頭，語氣專業流暢，需包含時間、規模、深度、震央位置及各地震度明細。
                
                請確保數字百分之百準確。
                """

                with st.spinner('AI 正在讀秒編稿中...'):
                    response = model.generate_content([prompt, image])
                    
                st.success("產出完畢！")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                st.info("小撇步：如果持續出現 404，請檢查 GitHub 的 requirements.txt 是否有正確寫入 google-generativeai")

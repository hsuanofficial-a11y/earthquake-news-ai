import streamlit as st
import google.generativeai as genai
from PIL import Image

# 頁面設定
st.set_page_config(page_title="地震速報文稿產生器", layout="centered")

st.title("🌋 地震速報文稿產生器")
st.write("上傳氣象署地震圖卡，自動生成主播稿與標題。")

# 側邊欄：設定 API Key
with st.sidebar:
    api_key = st.text_input("請輸入您的 Gemini API Key", type="password")
    st.info("您可以從 Google AI Studio 取得免費的 API Key。")

# 上傳元件
uploaded_file = st.file_uploader("選擇地震圖卡 (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 顯示上傳的圖片
    image = Image.open(uploaded_file)
    st.image(image, caption="已上傳的地震圖卡", use_container_width=True)
    
    if st.button("開始生成文稿"):
        if not api_key:
            st.error("請先在側邊欄輸入 API Key！")
        else:
            try:
                # 配置 Gemini
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash') # 使用輕快且強大的 flash 模型

                # 設定指令 (Prompt)
                prompt = """
                你是一位專業的新聞編稿人員。請根據上傳的地震速報圖卡內容，嚴格依照以下格式生成標題與主播稿：
                
                【新聞主播文稿格式】
                最新消息，根據氣象署最新資訊，今天[日期]稍早[時間]發生芮氏規模[數字]地震，地震深度[數字]公里，震央位於[地點]，位於[特定區域]。
                最大震度方面，在[縣市地點]有[數字]級，[縣市地點]有[數字]級...（列出所有震度點）。
                
                【新聞標題格式】
                [時間][地點]規模[數字]地震 最大震度[數字]級
                
                注意事項：
                1. 數字與地點必須準確。
                2. 語氣要專業且流暢。
                3. 如果有1級的地方，可以彙整在最後一段。
                """

                with st.spinner('AI 正在讀圖編稿中...'):
                    # 呼叫 AI
                    response = model.generate_content([prompt, image])
                    
                st.success("生成成功！")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"發生錯誤：{e}")

# 頁尾標示
st.caption("Developed for Hackathon | Powered by Gemini API")

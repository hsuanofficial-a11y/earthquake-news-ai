# 在程式最上方定義一個快取函數
@st.cache_data(show_spinner=False)
def get_ai_response(api_key, model_name, prompt, image):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([prompt, image])
    return response.text

# 在原本點擊按鈕的地方改寫成：
if st.button("🚀 產出主播稿"):
    try:
        # 使用快取函數，同樣的圖片不會重複扣額度
        result = get_ai_response(API_KEY, target_model, prompt, image)
        st.success("產出成功！")
        st.markdown("---")
        st.write(result)
    except Exception as e:
        if "429" in str(e):
            st.error("站住！AI 正在喘氣中... 這是免費版的次數限制。")
            st.warning("請現場靜候 20 秒，然後再試一次。")
        else:
            st.error(f"錯誤：{e}")

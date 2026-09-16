import streamlit as st
import pandas as pd
import base64
from openai import OpenAI

# 頁面基礎設定
st.set_page_config(page_title="333radiance 靜心空間", page_icon="✨", layout="centered")

# 華德福色彩 + Chiron GoRound TC 特粗體 + 版面完全置中
st.markdown("""
    <style>
    /* 引入 Chiron GoRound TC / HK 特粗字型 */
    @import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+HK:wght@800;900&family=Chiron+GoRound+TC:wght@800;900&display=swap');

    /* 強制整體背景為華德福暖奶油白 */
    .stApp {
        background-color: #FAF6EE !important;
    }

    /* 全局套用 Chiron GoRound TC 特粗字體與深黑字色 */
    html, body, [class*="st-"], .stMarkdown, p, span, div, h1, h2, h3, button, a {
        font-family: 'Chiron GoRound TC', 'Chiron GoRound HK', sans-serif !important;
        font-weight: 900 !important;
        color: #1F1F1F !important;
        text-align: center !important;
    }
    
    /* 大標題設定 */
    h1, .stTitle {
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
        margin-bottom: 0px !important;
        text-align: center !important;
    }

    /* 副標題設定 */
    p {
        font-size: 0.95rem !important;
        margin-top: 5px !important;
        margin-bottom: 15px !important;
        color: #222222 !important;
        text-align: center !important;
    }

    /* 華德福暖沙色特粗按鈕 */
    .stButton>button, .stLinkButton>a {
        border-radius: 20px !important;
        background-color: #EAD8C8 !important;
        color: #1F1F1F !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        text-align: center !important;
        justify-content: center !important;
    }

    /* AI 指引區塊：華德福草本淡綠（保持靠左閱讀） */
    .stSuccess {
        background-color: #EAF2E8 !important;
        color: #1B3B1E !important;
        border-radius: 14px !important;
        border: 1px solid #D2E3CF !important;
        text-align: left !important;
    }

    /* 隱藏原生選單與頁尾 */
    #MainMenu, footer, header, .stAppHeader {
        display: none !important;
    }

    /* 桌面端與手機端容器置中設定 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 410px !important;
        margin: 0 auto !important; /* 確保電腦觀看時整體容器置中 */
    }
    </style>
""", unsafe_allow_html=True)

# 使用 Base64 行內 CSS 確保圖片絕對置中
def render_centered_image(image_path, max_width=280):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin: 10px auto;">
                <img src="data:image/png;base64,{encoded_string}" style="max-width: {max_width}px; width: 100%; height: auto; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: block; margin: 0 auto;">
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        st.warning(f"請確保 GitHub 根目錄已上傳 {image_path}")

# 讀取卡片資料
@st.cache_data
def load_cards():
    return pd.read_csv("cards.csv")

try:
    df = load_cards()
except Exception:
    df = None

# 初始化頁面狀態
if "page" not in st.session_state:
    st.session_state.page = 0

# ==========================================
# 畫面 1：首頁
# ==========================================
if st.session_state.page == 0:
    st.markdown("<h1>✨ 333radiance 靜心陪伴空間</h1>", unsafe_allow_html=True)
    st.markdown("<p>外面的世界或有紛擾，這裡為你留有一處安全空間。</p>", unsafe_allow_html=True)
    
    render_centered_image("card_001.png", max_width=280)
    
    st.write("")
    
    if st.button("✨ 抽一張靜心卡", use_container_width=True):
        if df is not None:
            st.session_state.selected_card = df.sample(1).iloc[0]
            st.session_state.page = 1
            st.rerun()
        else:
            st.error("請確保 GitHub 上已建立 cards.csv")

# ==========================================
# 畫面 2：抽卡結果頁
# ==========================================
elif st.session_state.page == 1:
    card = st.session_state.selected_card
    card_filename = f"{card['card_id']}.png"
    
    render_centered_image(card_filename, max_width=280)
    
    # 呼叫 DeepSeek API
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if api_key:
        with st.spinner("陪伴員正在準備指引..."):
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                context = card.get('prompt_context', '正在觀看這張靜心圖卡，需要休息與安心')
                
                system_prompt = (
                    "你現在是 333radiance 的靜心陪伴員。"
                    f"使用者現在{context}。"
                    "請用 1 句話（20 字以內，必須使用香港繁體中文，必須書面語），給他一個引導視線聚焦或呼吸的指示。"
                    "語氣溫柔，要10歲的小孩都可以理解的文字，不作任何醫療建議。"
                )

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": "請給我一句靜心指示。"}
                    ],
                    max_tokens=50,
                    temperature=0.7
                )
                
                st.success(f"✨ **靜心指引：** {response.choices[0].message.content}")
                
            except Exception as e:
                st.error("系統繁忙中，請深深呼吸，好好照顧自己。")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 再抽一張", use_container_width=True):
            st.session_state.page = 0
            st.rerun()
            
    with col2:
        st.link_button("👉 探索 IG", "https://www.instagram.com/333radiance/", use_container_width=True)

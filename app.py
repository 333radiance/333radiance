import streamlit as st
import pandas as pd
from openai import OpenAI

# 頁面基礎設定
st.set_page_config(page_title="333radiance 靜心空間", page_icon="✨", layout="centered")

# 華德福色彩與版面注入 (網頁背景暖白、標題縮小、文字純黑)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Zen+MaruGothic:wght@400;500;700&display=swap');

    /* 強制整體背景為華德福暖奶油白 */
    .stApp {
        background-color: #FAF6EE !important;
    }

    /* 統一字型與黑字設定，確保高對比清晰度 */
    html, body, [class*="st-"], .stMarkdown, p, span, div {
        font-family: 'Zen Maru Gothic', sans-serif !important;
        color: #1F1F1F !important;
    }

    /* 大標題改細、改小 */
    h1, .stTitle {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #222222 !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.3rem !important;
    }

    /* 華德福暖沙色按鈕 */
    .stButton>button, .stLinkButton>a {
        border-radius: 20px !important;
        background-color: #EAD8C8 !important;
        color: #222222 !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }

    /* AI 指引區塊：華德福草本淡綠 */
    .stSuccess {
        background-color: #EAF2E8 !important;
        color: #1B3B1E !important;
        border-radius: 14px !important;
        border: 1px solid #D2E3CF !important;
    }

    /* 隱藏原生選單與頁尾 */
    #MainMenu, footer, header, .stAppHeader {
        display: none !important;
    }

    /* 手機螢幕寬度與圖片佈局優化 */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1rem !important;
        max-width: 410px !important;
    }

    img {
        width: 100% !important;
        max-width: 280px !important;
        height: auto !important;
        margin: 0 auto !important;
        display: block !important;
        border-radius: 16px;
    }
    </style>
""", unsafe_allow_html=True)

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
    st.title("✨ 333radiance 靜心陪伴空間")
    st.write("外面的世界或有紛擾，這裡為你留有一處安全空間。")
    
    try:
        st.image("card_001.png", use_container_width=True)
    except Exception:
        st.info("🖼️ 請確保已上傳 card_001.png")
    
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
    
    try:
        st.image(card_filename, use_container_width=True)
    except Exception:
        st.warning(f"請確保已上傳 {card_filename}")
    
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

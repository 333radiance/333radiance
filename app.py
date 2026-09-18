import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# 1. 頁面基本設定
st.set_page_config(
    page_title="333 Radiance | 靜心空間",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 高質感自訂 CSS 樣式
st.markdown("""
    <!-- 引入 Chiron GoRound TC 官方 GitHub CDN (包含常規體與特粗體) -->
    <style>
    @import url('https://cdn.jsdelivr.net/gh/chiron-fonts/chiron-go-round-tc@v1.000/webfonts/ChironGoRoundTC-Regular.css');
    @import url('https://cdn.jsdelivr.net/gh/chiron-fonts/chiron-go-round-tc@v1.000/webfonts/ChironGoRoundTC-ExtraBold.css');

    /* 全局字體設定：強制套用 Chiron GoRound TC 常規體 (400) */
    html, body, [class*="css"], .stApp, p, div, span, input {
        font-family: 'Chiron GoRound TC', 'Chiron GoRound HK', sans-serif !important;
        font-weight: 400 !important;
        background-color: #F9F6F0;
        color: #38332F;
    }
    
    /* 隱藏預設 Streamlit 頂部與底部元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 首頁日期 (特粗) */
    .date-text {
        font-weight: 900 !important;
        text-align: center !important; 
        color: #8A9A86; 
        font-size: 1.05rem;
        letter-spacing: 2px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* 首頁情境問候語 (特粗) */
    .welcome-text {
        font-weight: 900 !important;
        text-align: center !important; 
        color: #38332F; 
        font-size: 1.15rem;
        line-height: 1.7;
        margin-top: 1.2rem;
        margin-bottom: 2.5rem;
        padding: 0 1rem;
    }
    
    /* === 第二頁排版優化 (字體調細 1-2 級) === */
    .quote-text {
        font-weight: 400 !important; /* 恢復正常粗幼 */
        font-size: 0.92rem !important; /* 字體微調縮小，更顯細緻 */
        line-height: 1.85;
        color: #2B2927;
        padding: 1.6rem;
        background-color: #F0EAE1;
        border-radius: 12px;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        text-align: justify;
        letter-spacing: 0.5px;
    }
    
    .guide-box {
        font-weight: 400 !important;
        font-size: 0.88rem !important; /* 引導內文再細一點 */
        line-height: 1.75;
        color: #4A4541;
        padding: 1.2rem;
        border-left: 3.5px solid #8A9A86;
        background-color: transparent;
        margin-bottom: 2rem;
    }
    
    .guide-title {
        font-weight: 900 !important;
        font-size: 0.9rem !important;
        color: #8A9A86;
        margin-bottom: 0.6rem;
        letter-spacing: 1.5px;
    }
    
    /* === 容器強制置中 === */
    [data-testid="stColumn"], div.stButton, .ig-btn-container, .element-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }

    /* === 按鈕共用樣式 (確保 Streamlit 按鈕與 IG 按鈕 100% 一致) === */
    div.stButton > button, .ig-button {
        font-family: 'Chiron GoRound TC', 'Chiron GoRound HK', sans-serif !important;
        font-weight: 900 !important;
        background-color: #38332F !important;
        color: #F9F6F0 !important;
        border: none !important;
        border-radius: 25px !important;
        height: 3.2rem !important; /* 統一固定高度 */
        font-size: 1.05rem !important;
        letter-spacing: 1.5px !important;
        margin: 0 auto !important;
        width: 100% !important;
        max-width: 240px !important; /* 統一最大寬度 */
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-decoration: none !important;
        /* 加入平滑漸變過渡效果 */
        transition: background-color 0.4s ease, transform 0.3s ease, box-shadow 0.3s ease !important;
        cursor: pointer !important;
    }

    /* === 按鈕懸停漸變與浮動效果 === */
    div.stButton > button:hover, .ig-button:hover {
        background-color: #635C55 !important; /* 顏色平滑過渡變淺 */
        color: #ffffff !important;
        transform: translateY(-3px) !important; /* 微微上浮 */
        box-shadow: 0 6px 15px rgba(56, 51, 47, 0.25) !important; /* 增加漸變陰影 */
    }
    </style>
""", unsafe_allow_html=True)

# 3. 讀取本地資料庫
@st.cache_data
def load_data():
    try:
        quotes_df = pd.read_csv("quotes.csv")
        guides_df = pd.read_csv("guides.csv")
        greetings_df = pd.read_csv("greetings.csv") if os.path.exists("greetings.csv") else pd.DataFrame()
        return quotes_df, guides_df, greetings_df
    except Exception as e:
        st.error("載入 CSV 資料庫時發生錯誤，請檢查檔案格式。")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

quotes_df, guides_df, greetings_df = load_data()

# 4. 初始化 Session State
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'home'
if 'selected_quote' not in st.session_state:
    st.session_state.selected_quote = ""
if 'selected_guide' not in st.session_state:
    st.session_state.selected_guide = ""
if 'selected_greeting' not in st.session_state:
    st.session_state.selected_greeting = ""
if 'selected_cover_path' not in st.session_state:
    st.session_state.selected_cover_path = ""
if 'selected_image_path' not in st.session_state:
    st.session_state.selected_image_path = ""

def get_today_string():
    now = datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_str = weekdays[now.weekday()]
    return f"{now.year}年{now.month}月{now.day}日 {weekday_str}"

def get_random_image_from_folder(folder_name):
    if os.path.exists(folder_name):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
        images = [f for f in os.listdir(folder_name) if f.lower().endswith(valid_extensions)]
        if images:
            return os.path.join(folder_name, random.choice(images))
    return ""

# 5. 核心邏輯函數
def init_home_data():
    st.session_state.selected_cover_path = get_random_image_from_folder("covers")
    if not greetings_df.empty:
        st.session_state.selected_greeting = random.choice(greetings_df['text'].tolist())
    else:
        st.session_state.selected_greeting = "或許今天的你，會需要一點心靈的平靜。"

def draw_card():
    if not quotes_df.empty:
        st.session_state.selected_quote = random.choice(quotes_df['text'].tolist())
    if not guides_df.empty:
        st.session_state.selected_guide = random.choice(guides_df['text'].tolist())
            
    st.session_state.selected_image_path = get_random_image_from_folder("cards")
    st.session_state.current_stage = 'result'

def reset_app():
    init_home_data()
    st.session_state.current_stage = 'home'

if not st.session_state.selected_greeting:
    init_home_data()

# 6. 介面渲染
if st.session_state.current_stage == 'home':
    today_str = get_today_string()
    
    st.markdown(f"<div class='date-text'>今日是 {today_str}</div>", unsafe_allow_html=True)
    
    if st.session_state.selected_cover_path and os.path.exists(st.session_state.selected_cover_path):
        st.image(st.session_state.selected_cover_path, use_container_width=True)
    
    st.markdown(f"<div class='welcome-text'>{st.session_state.selected_greeting}</div>", unsafe_allow_html=True)
    
    if st.button("開啟今日指引"):
        draw_card()
        st.rerun()

elif st.session_state.current_stage == 'result':
    if st.session_state.selected_image_path and os.path.exists(st.session_state.selected_image_path):
        st.image(st.session_state.selected_image_path, use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; padding:3rem; background:#E6E2DD; border-radius:12px; margin-bottom:1.5rem; color:#8A9A86;'>[ 請確保 cards 資料夾內有放入圖片 ]</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='quote-text'>{st.session_state.selected_quote}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='guide-box'>
            <div class='guide-title'>✦ 給此刻的你</div>
            {st.session_state.selected_guide}
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 底部按鈕排版
    col1, col2 = st.columns(2)
    with col1:
        if st.button("換個視角"):
            reset_app()
            st.rerun()
    with col2:
        st.markdown("""
            <div class="ig-btn-container">
                <a href="https://instagram.com" target="_blank" class="ig-button">
                    關注 IG
                </a>
            </div>
        """, unsafe_allow_html=True)

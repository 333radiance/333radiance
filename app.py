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

# 2. 簡潔高質感 CSS 樣式 (使用系統預設字體，按鈕與排版完美對齊)
st.markdown("""
    <style>
    /* 基礎背景與顏色 */
    html, body, .stApp {
        background-color: #F9F6F0 !important;
        color: #38332F !important;
    }
    
    /* 隱藏預設 Streamlit 頂部與底部元素 */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 日期與問候語 */
    .date-text {
        text-align: center !important; 
        color: #8A9A86; 
        font-size: 1.05rem;
        letter-spacing: 2px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .welcome-text {
        text-align: center !important; 
        color: #38332F; 
        font-size: 1.15rem;
        line-height: 1.7;
        margin-top: 1.2rem;
        margin-bottom: 2.5rem;
        padding: 0 1rem;
    }
    
    /* 金句與引導區塊 */
    .quote-text {
        font-size: 1rem !important;
        line-height: 1.85;
        color: #2B2927;
        padding: 1.6rem;
        background-color: #F0EAE1;
        border-radius: 12px;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        text-align: justify;
    }
    
    .guide-box {
        font-size: 0.95rem !important;
        line-height: 1.75;
        color: #4A4541;
        padding: 1.2rem;
        border-left: 3.5px solid #8A9A86;
        margin-bottom: 2rem;
    }
    
    .guide-title {
        font-size: 0.95rem !important;
        color: #8A9A86;
        margin-bottom: 0.6rem;
    }
    
    /* 按鈕容器置中 */
    div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    .ig-btn-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 5px !important;
    }

    /* 兩個按鈕外觀 100% 一致與漸變過渡效果 */
    div[data-testid="stButton"] button, a.ig-button {
        background-color: #38332F !important;
        color: #F9F6F0 !important;
        border: none !important;
        border-radius: 30px !important;
        width: 100% !important;
        max-width: 250px !important;
        height: 50px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        margin: 0 auto !important;
        font-size: 1.05rem !important;
        letter-spacing: 1.5px !important;
    }

    div[data-testid="stButton"] button p {
        color: #F9F6F0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 滑鼠懸停浮動與漸變 */
    div[data-testid="stButton"] button:hover, a.ig-button:hover {
        background-color: #5A544D !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(56, 51, 47, 0.2) !important;
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
    
    if st.button("開啟今日指引", use_container_width=True):
        draw_card()
        st.rerun()

elif st.session_state.current_stage == 'result':
    if st.session_state.selected_image_path and os.path.exists(st.session_state.selected_image_path):
        st.image(st.session_state.selected_image_path, use_container_width=True)
    
    st.markdown(f"<div class='quote-text'>{st.session_state.selected_quote}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='guide-box'>
            <div class='guide-title'>✦ 給此刻的你</div>
            {st.session_state.selected_guide}
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("換個視角", use_container_width=True):
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

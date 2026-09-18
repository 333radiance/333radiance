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

# 2. 高質感自訂 CSS 樣式 (載入 Chiron GoRound TC 字體與手機優化)
st.markdown("""
    <!-- 引入 Google Fonts / Google 開源字體 Chiron GoRound HK / TC 質感圓黑體 -->
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+HK:wght@400;700;900&display=swap');

    /* 全局字體設定：主要字體選用 Chiron GoRound HK/TC */
    html, body, [class*="css"], .stApp {
        font-family: 'Chiron GoRound HK', 'Chiron GoRound TC', 'PingFang HK', 'Microsoft JhengHei', sans-serif !important;
        background-color: #F9F6F0;
        color: #38332F;
    }
    
    /* 隱藏預設的 Streamlit 頂部與底部元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 標題與重點文字使用 Chiron GoRound TC 特粗體 (900) */
    h1, h2, h3, .heavy-font, .guide-title, .date-text {
        font-family: 'Chiron GoRound HK', 'Chiron GoRound TC', sans-serif !important;
        font-weight: 900 !important;
    }

    /* 首頁日期 */
    .date-text {
        text-align: center; 
        color: #8A9A86; 
        font-size: 1.05rem;
        letter-spacing: 2px;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* 首頁情境問候語 (精緻適中大小) */
    .welcome-text {
        text-align: center; 
        color: #38332F; 
        font-size: 1.15rem;
        line-height: 1.7;
        margin-top: 1.2rem;
        margin-bottom: 2.5rem;
        font-weight: 700;
        padding: 0 1rem;
    }
    
    /* 結果頁金句排版 (文字細緻化，適合手機閱讀) */
    .quote-text {
        font-size: 0.98rem;
        line-height: 1.85;
        font-weight: 400;
        color: #2B2927;
        padding: 1.6rem;
        background-color: #F0EAE1;
        border-radius: 12px;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        text-align: justify;
        letter-spacing: 0.3px;
    }
    
    /* 靜心引導排版 */
    .guide-box {
        font-size: 0.95rem;
        line-height: 1.75;
        color: #4A4541;
        padding: 1.2rem;
        border-left: 3.5px solid #8A9A86;
        background-color: transparent;
        margin-bottom: 2rem;
    }
    
    .guide-title {
        font-size: 0.88rem;
        color: #8A9A86;
        margin-bottom: 0.6rem;
        letter-spacing: 1.5px;
    }
    
    /* 置中按鈕美化 (特粗字體) */
    .stButton>button {
        font-family: 'Chiron GoRound HK', 'Chiron GoRound TC', sans-serif !important;
        font-weight: 900 !important;
        background-color: #38332F;
        color: #F9F6F0;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 1.5px;
        display: block;
        margin: 0 auto;
    }
    .stButton>button:hover {
        background-color: #5A544D;
        color: #ffffff;
    }

    /* 外連 IG 置中按鈕樣式 */
    .ig-button {
        font-family: 'Chiron GoRound HK', 'Chiron GoRound TC', sans-serif !important;
        font-weight: 900 !important;
        display: block;
        width: 100%;
        text-align: center;
        background-color: transparent;
        color: #38332F;
        border: 1.5px solid #38332F;
        border-radius: 25px;
        padding: 0.68rem 0;
        font-size: 1rem;
        text-decoration: none;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .ig-button:hover {
        background-color: #38332F;
        color: #F9F6F0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 讀取本地資料庫 (使用快取提升載入速度)
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

# 獲取今日日期字串
def get_today_string():
    now = datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_str = weekdays[now.weekday()]
    return f"{now.year}年{now.month}月{now.day}日 {weekday_str}"

# 隨機取得資料夾中的圖片
def get_random_image_from_folder(folder_name):
    if os.path.exists(folder_name):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
        images = [f for f in os.listdir(folder_name) if f.lower().endswith(valid_extensions)]
        if images:
            return os.path.join(folder_name, random.choice(images))
    return ""

# 5. 核心邏輯函數
def init_home_data():
    # 每次回首頁，自動抽換首頁 cover 橫圖與情境問候語
    st.session_state.selected_cover_path = get_random_image_from_folder("covers")
    if not greetings_df.empty:
        st.session_state.selected_greeting = random.choice(greetings_df['text'].tolist())
    else:
        st.session_state.selected_greeting = "或許今天的你，會需要一點心靈的指引。"

def draw_card():
    # 隨機抽取金句
    if not quotes_df.empty:
        st.session_state.selected_quote = random.choice(quotes_df['text'].tolist())
    
    # 隨機抽取靜心引導
    if not guides_df.empty:
        st.session_state.selected_guide = random.choice(guides_df['text'].tolist())
            
    # 隨機抽取結果頁橫圖
    st.session_state.selected_image_path = get_random_image_from_folder("cards")
    
    # 切換頁面狀態
    st.session_state.current_stage = 'result'

def reset_app():
    init_home_data()
    st.session_state.current_stage = 'home'

# 首次載入首頁資料
if not st.session_state.selected_greeting:
    init_home_data()

# 6. 介面渲染
if st.session_state.current_stage == 'home':
    today_str = get_today_string()
    
    # 首頁日期
    st.markdown(f"<div class='date-text'>今日是 {today_str}</div>", unsafe_allow_html=True)
    
    # 首頁隨機橫向封面圖 (covers 資料夾)
    if st.session_state.selected_cover_path and os.path.exists(st.session_state.selected_cover_path):
        st.image(st.session_state.selected_cover_path, use_container_width=True)
    
    # 首頁情境問候語
    st.markdown(f"<div class='welcome-text'>{st.session_state.selected_greeting}</div>", unsafe_allow_html=True)
    
    # 完美置中的「抽取今日卡片」按鈕
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("抽取今日卡片"):
            draw_card()
            st.rerun()

elif st.session_state.current_stage == 'result':
    # 結果頁打橫卡片圖 (cards 資料夾)
    if st.session_state.selected_image_path and os.path.exists(st.session_state.selected_image_path):
        st.image(st.session_state.selected_image_path, use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; padding:3rem; background:#E6E2DD; border-radius:12px; margin-bottom:1.5rem; color:#8A9A86;'>[ 請確保 cards 資料夾內有放入橫向圖片 ]</div>", unsafe_allow_html=True)
    
    # 顯示金句 (字體調細、適中排版)
    st.markdown(f"<div class='quote-text'>{st.session_state.selected_quote}</div>", unsafe_allow_html=True)
    
    # 顯示靜心引導 
    st.markdown(f"""
        <div class='guide-box'>
            <div class='guide-title'>✦ 給此刻的你</div>
            {st.session_state.selected_guide}
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 底部按鈕：雙按鈕並排且精準置中
    col1, col2 = st.columns(2)
    with col1:
        if st.button("重新開始"):
            reset_app()
            st.rerun()
    with col2:
        st.markdown("""
            <a href="https://instagram.com" target="_blank" class="ig-button">
                關注 IG
            </a>
        """, unsafe_allow_html=True)

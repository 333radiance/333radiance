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
    <style>
    /* 全局字體與背景 */
    .stApp {
        background-color: #F9F6F0;
        color: #38332F;
        font-family: 'Helvetica Neue', Helvetica, 'PingFang HK', 'Microsoft JhengHei', sans-serif;
    }
    
    /* 隱藏預設的 Streamlit 頂部與底部元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 首頁日期與標題 */
    .date-text {
        text-align: center; 
        color: #8A9A86; 
        font-size: 1.1rem;
        font-weight: 500;
        letter-spacing: 2px;
        margin-top: 3rem;
    }
    .welcome-text {
        text-align: center; 
        color: #38332F; 
        font-size: 1.8rem;
        line-height: 1.6;
        margin-top: 1.5rem;
        margin-bottom: 4rem;
        font-weight: 400;
    }
    
    /* 金句排版 */
    .quote-text {
        font-size: 1.15rem;
        line-height: 1.8;
        font-weight: 400;
        color: #2B2927;
        padding: 2rem;
        background-color: #F0EAE1;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: justify;
        letter-spacing: 0.5px;
    }
    
    /* 靜心引導排版 */
    .guide-box {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #4A4541;
        padding: 1.5rem;
        border-left: 3px solid #8A9A86;
        background-color: transparent;
        margin-bottom: 2rem;
    }
    
    .guide-title {
        font-size: 0.9rem;
        color: #8A9A86;
        font-weight: 600;
        margin-bottom: 0.8rem;
        letter-spacing: 1.5px;
    }
    
    /* 按鈕美化 */
    .stButton>button {
        background-color: #38332F;
        color: #F9F6F0;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #5A544D;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 讀取本地資料庫 
@st.cache_data
def load_data():
    try:
        quotes_df = pd.read_csv("quotes.csv")
        guides_df = pd.read_csv("guides.csv")
        return quotes_df, guides_df
    except FileNotFoundError:
        st.error("找不到 quotes.csv 或 guides.csv，請確保檔案已上傳。")
        return pd.DataFrame(), pd.DataFrame()

quotes_df, guides_df = load_data()

# 4. 初始化 Session State
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'home'
if 'selected_quote' not in st.session_state:
    st.session_state.selected_quote = ""
if 'selected_guide' not in st.session_state:
    st.session_state.selected_guide = ""
if 'selected_image_path' not in st.session_state:
    st.session_state.selected_image_path = ""

# 獲取今日日期字串
def get_today_string():
    now = datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_str = weekdays[now.weekday()]
    return f"{now.year}年{now.month}月{now.day}日 {weekday_str}"

# 5. 核心邏輯函數
def draw_card():
    # 隨機抽取金句
    if not quotes_df.empty:
        st.session_state.selected_quote = random.choice(quotes_df['text'].tolist())
    
    # 隨機抽取靜心引導
    if not guides_df.empty:
        st.session_state.selected_guide = random.choice(guides_df['text'].tolist())
            
    # 智能隨機抽取圖片 (自動掃描 cards 資料夾內的任何圖片)
    st.session_state.selected_image_path = ""
    if os.path.exists("cards"):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
        # 找出所有符合副檔名的檔案
        images = [f for f in os.listdir("cards") if f.lower().endswith(valid_extensions)]
        if images:
            # 隨機選一張並組合完整路徑
            selected_image = random.choice(images)
            st.session_state.selected_image_path = os.path.join("cards", selected_image)
    
    # 切換頁面狀態
    st.session_state.current_stage = 'result'

def reset_app():
    st.session_state.current_stage = 'home'

# 6. 介面渲染
if st.session_state.current_stage == 'home':
    today_str = get_today_string()
    
    # 首頁排版
    st.markdown(f"<div class='date-text'>今日是 {today_str}</div>", unsafe_allow_html=True)
    st.markdown("<div class='welcome-text'>或許今天的你，<br>會需要一點心靈的指引。</div>", unsafe_allow_html=True)
    
    # 置中按鈕
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("抽取今日卡片"):
            draw_card()
            st.rerun()

elif st.session_state.current_stage == 'result':
    # 顯示圖片 (有找到圖片就顯示，找不到就顯示灰色提示框)
    if st.session_state.selected_image_path and os.path.exists(st.session_state.selected_image_path):
        st.image(st.session_state.selected_image_path, use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; padding:4rem; background:#E6E2DD; border-radius:12px; margin-bottom:2rem; color:#8A9A86;'>[ 請確保 cards 資料夾內有放入圖片檔 ]</div>", unsafe_allow_html=True)
    
    # 顯示金句 
    st.markdown(f"<div class='quote-text'>{st.session_state.selected_quote}</div>", unsafe_allow_html=True)
    
    # 顯示靜心引導 
    st.markdown(f"""
        <div class='guide-box'>
            <div class='guide-title'>✦ 給此刻的你</div>
            {st.session_state.selected_guide}
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 底部按鈕
    col1, col2 = st.columns(2)
    with col1:
        if st.button("重新開始"):
            reset_app()
            st.rerun()
    with col2:
        st.markdown("""
            <a href="https://instagram.com" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: transparent; color: #38332F; border: 1px solid #38332F; border-radius: 8px; padding: 0.5rem 2rem; font-size: 1rem; cursor: pointer;">
                    關注 IG
                </button>
            </a>
        """, unsafe_allow_html=True)

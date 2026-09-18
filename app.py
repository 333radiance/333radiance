import streamlit as st
import pandas as pd
import random
import os

# 1. 頁面基本設定
st.set_page_config(
    page_title="333 Radiance | 靜心空間",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 高質感自訂 CSS 樣式 (溫暖、極簡、空間感)
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
    
    /* 金句排版 (引號與大字體) */
    .quote-text {
        font-size: 1.2rem;
        line-height: 1.8;
        font-weight: 400;
        color: #2B2927;
        padding: 2rem;
        background-color: #F0EAE1;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: justify;
        letter-spacing: 0.5px;
    }
    
    /* 靜心引導排版 */
    .guide-box {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #4A4541;
        padding: 1.5rem;
        border-left: 4px solid #8A9A86;
        background-color: transparent;
        margin-bottom: 2rem;
    }
    
    .guide-title {
        font-size: 0.9rem;
        color: #8A9A86;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    /* 按鈕美化 */
    .stButton>button {
        background-color: #38332F;
        color: #F9F6F0;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #5A544D;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 讀取本地資料庫 (使用快取提升載入速度)
@st.cache_data
def load_data():
    try:
        quotes_df = pd.read_csv("quotes.csv")
        guides_df = pd.read_csv("guides.csv")
        return quotes_df, guides_df
    except FileNotFoundError:
        st.error("找不到 quotes.csv 或 guides.csv，請確保檔案已上傳至專案目錄。")
        return pd.DataFrame(), pd.DataFrame()

quotes_df, guides_df = load_data()

# 4. 初始化 Session State
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'home'
if 'selected_quote' not in st.session_state:
    st.session_state.selected_quote = ""
if 'selected_guide' not in st.session_state:
    st.session_state.selected_guide = ""
if 'selected_image_id' not in st.session_state:
    st.session_state.selected_image_id = 1

# 5. 核心邏輯函數
def draw_card(user_need):
    # 隨機抽取金句
    if not quotes_df.empty:
        st.session_state.selected_quote = random.choice(quotes_df['text'].tolist())
    
    # 根據使用者的「需要」篩選並隨機抽取靜心引導
    if not guides_df.empty:
        filtered_guides = guides_df[guides_df['category'] == user_need]
        if not filtered_guides.empty:
            st.session_state.selected_guide = random.choice(filtered_guides['text'].tolist())
        else:
            st.session_state.selected_guide = random.choice(guides_df['text'].tolist()) # 防呆機制
            
    # 隨機抽取圖片 ID (假設你有 1~99 張圖片在 cards/ 資料夾中)
    st.session_state.selected_image_id = random.randint(1, 99)
    
    # 切換頁面狀態
    st.session_state.current_stage = 'result'

def reset_app():
    st.session_state.current_stage = 'home'

# 6. 介面渲染
if st.session_state.current_stage == 'home':
    st.markdown("<h2 style='text-align: center; color: #38332F; margin-top: 2rem;'>333 Radiance</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>給自己一個安靜的片刻</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    if not guides_df.empty:
        # 動態抓取 guides.csv 裡面的所有「需要」類別
        needs_options = guides_df['category'].unique().tolist()
        
        st.markdown("#### 你當下最需要什麼？")
        user_need = st.selectbox("請選擇一個最貼近你目前狀態的選項：", needs_options, label_visibility="collapsed")
        
        st.write("")
        st.write("")
        
        if st.button("抽取今日指引"):
            draw_card(user_need)
            st.rerun()

elif st.session_state.current_stage == 'result':
    # 顯示圖片 (這裡假設圖片命名格式為 card_001.jpg 到 card_099.jpg)
    image_filename = f"cards/card_{st.session_state.selected_image_id:03d}.jpg"
    
    # 檢查圖片是否存在，若無則顯示佔位文字
    if os.path.exists(image_filename):
        st.image(image_filename, use_container_width=True)
    else:
        st.markdown(f"<div style='text-align:center; padding:4rem; background:#E6E2DD; border-radius:12px; margin-bottom:2rem;'>圖片 {image_filename} 將顯示於此</div>", unsafe_allow_html=True)
    
    # 顯示金句 (Story & Wisdom)
    st.markdown(f"<div class='quote-text'>{st.session_state.selected_quote}</div>", unsafe_allow_html=True)
    
    # 顯示靜心引導 (Modern Explanation / Action)
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
        # Instagram 連結按鈕 (使用 markdown 模擬按鈕樣式)
        st.markdown("""
            <a href="https://instagram.com" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: transparent; color: #38332F; border: 1px solid #38332F; border-radius: 8px; padding: 0.5rem 2rem; font-size: 1rem; cursor: pointer;">
                    關注 IG
                </button>
            </a>
        """, unsafe_allow_html=True)

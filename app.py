import streamlit as st
import pandas as pd
from openai import OpenAI

# 頁面基礎設定
st.set_page_config(page_title="333radiance 靜心空間", page_icon="✨", layout="centered")

# 隱藏預設頁首頁尾，提升視覺純粹感
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 讀取 100 張卡片資料
@st.cache_data
def load_cards():
    return pd.read_csv("cards.csv")

try:
    df = load_cards()
except Exception:
    df = None

# 初始化頁面狀態 (0: 畫面1 首頁, 1: 畫面2 抽卡結果頁)
if "page" not in st.session_state:
    st.session_state.page = 0

# ==========================================
# 畫面 1：首頁（迎賓 + 封面 + 抽卡按鈕）
# ==========================================
if st.session_state.page == 0:
    st.title("✨ 333radiance 靜心陪伴空間")
    st.write("外面的世界或許紛亂，這裡為你留有一處安全空間。抽一張卡，收下今日的溫柔與平靜。")
    
    # 顯示封面圖
    try:
        st.image("cover.png", use_container_width=True)
    except Exception:
        st.info("🖼️ （請在上傳封面圖至 GitHub，檔名設為 cover.png）")
    
    st.write("") # 增加間距
    
    if st.button("✨ 抽一張靜心卡", use_container_width=True):
        if df is not None:
            # 隨機抽取 1 張卡片並跳轉
            st.session_state.selected_card = df.sample(1).iloc[0]
            st.session_state.page = 1
            st.rerun()
        else:
            st.error("請確保 GitHub 上已建立 cards.csv 資料表。")

# ==========================================
# 畫面 2：抽卡結果頁（卡片 + AI 陪伴語 + IG 連結 / 再抽一次）
# ==========================================
elif st.session_state.page == 1:
    card = st.session_state.selected_card
    
    # 1. 顯示抽到的卡片圖片
    try:
        st.image(f"images/{card['card_id']}.png", use_container_width=True)
    except Exception:
        st.warning(f"圖片載入中，請確保 images/{card['card_id']}.png 已存在。")
    
    # 2. 呼叫 DeepSeek API 生成 20 字內香港繁體字陪伴語
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if api_key:
        with st.spinner("333radiance 陪伴員正在為你準備指引..."):
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                # 取得該卡片的情境引導（若 CSV 沒填則用預設值）
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
                
                ai_message = response.choices[0].message.content
                st.success(f"✨ **靜心指引：** {ai_message}")
                
            except Exception as e:
                st.error("系統繁忙中，請深深呼吸，好好照顧自己。")
    else:
        st.info("💡 請在 Streamlit Secrets 中設定 DEEPSEEK_API_KEY。")

    st.divider()
    
    # 3. 按鈕區：再抽一次 / 前往 IG
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 再抽一張", use_container_width=True):
            st.session_state.page = 0
            st.rerun()
            
    with col2:
        st.link_button("👉 探索 333radiance IG", "https://www.instagram.com/333radiance/", use_container_width=True)

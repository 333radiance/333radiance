import streamlit as st
import pandas as pd
import base64
import os
import json
import streamlit.components.v1 as components
from openai import OpenAI

# 頁面基礎設定
st.set_page_config(page_title="333radiance 靜心空間", page_icon="✨", layout="centered")

# 華德福色彩 + Chiron GoRound TC 特粗體
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chiron+GoRound+HK:wght@800;900&family=Chiron+GoRound+TC:wght@800;900&display=swap');

    .stApp {
        background-color: #FAF6EE !important;
    }

    html, body, [class*="st-"], .stMarkdown, p, span, div, h1, h2, h3, button, a {
        font-family: 'Chiron GoRound TC', 'Chiron GoRound HK', sans-serif !important;
        font-weight: 900 !important;
        color: #1F1F1F !important;
        text-align: center !important;
    }
    
    h1, .stTitle {
        font-size: 1.35rem !important;
        font-weight: 900 !important;
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
        margin-bottom: 0px !important;
        text-align: center !important;
    }

    p {
        font-size: 0.92rem !important;
        margin-top: 4px !important;
        margin-bottom: 10px !important;
        color: #222222 !important;
        text-align: center !important;
    }

    /* 靜心金句框 */
    .quote-box {
        background-color: #F5EBE1;
        border-radius: 14px;
        padding: 12px 16px;
        margin: 10px 0;
        font-size: 0.98rem;
        font-weight: 800;
        color: #3D2C2E;
        line-height: 1.45;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    /* 華德福暖沙色按鈕 */
    .stButton>button, .stLinkButton>a {
        border-radius: 18px !important;
        background-color: #EAD8C8 !important;
        color: #1F1F1F !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 0.9rem !important;
        padding: 0.45rem 0.6rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        text-align: center !important;
        justify-content: center !important;
    }

    /* AI 指引區塊 */
    .stSuccess {
        background-color: #EAF2E8 !important;
        color: #1B3B1E !important;
        border-radius: 12px !important;
        border: 1px solid #D2E3CF !important;
        padding: 12px 14px !important;
        margin-top: 8px !important;
        margin-bottom: 12px !important;
        text-align: left !important;
        font-size: 0.92rem !important;
    }

    /* 隱藏原生選單、頁尾及右下角官方浮動工具列 */
    #MainMenu, footer, header, .stAppHeader,
    [data-testid="stStatusWidget"],
    [data-testid="manage-app-button"],
    .stAppDeployButton,
    div[class*="viewerBadge"] {
        display: none !important;
    }

    /* 手機端容器優化 */
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 390px !important;
        margin: 0 auto !important;
    }

    /* 調整元件之間的垂直間距 */
    [data-testid="stVerticalBlock"] {
        gap: 0.8rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# 置中渲染圖片
def render_centered_image(image_name, max_width=240):
    possible_paths = [
        image_name,
        os.path.join("cards", image_name)
    ]
    
    target_path = None
    for path in possible_paths:
        if os.path.exists(path):
            target_path = path
            break

    if target_path:
        with open(target_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin: 6px auto;">
                <img src="data:image/png;base64,{encoded_string}" style="max-width: {max_width}px; width: 100%; height: auto; border-radius: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.04); display: block; margin: 0 auto;">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"請確保已上傳 {image_name}")

# 強制讀取 CSV
def load_data():
    try:
        cards_df = pd.read_csv("cards.csv", encoding="utf-8-sig") if os.path.exists("cards.csv") else None
    except Exception:
        cards_df = pd.read_csv("cards.csv") if os.path.exists("cards.csv") else None

    try:
        quotes_df = pd.read_csv("quotes.csv", encoding="utf-8-sig") if os.path.exists("quotes.csv") else None
    except Exception:
        quotes_df = pd.read_csv("quotes.csv") if os.path.exists("quotes.csv") else None

    return cards_df, quotes_df

df_cards, df_quotes = load_data()

if "page" not in st.session_state:
    st.session_state.page = 0

# ==========================================
# 畫面 1：首頁
# ==========================================
if st.session_state.page == 0:
    st.markdown("<h1>✨ 333radiance 靜心空間</h1>", unsafe_allow_html=True)
    st.markdown("<p>外面的世界或有紛擾，這裡為你留有一處安全空間。</p>", unsafe_allow_html=True)
    
    render_centered_image("card_001.png", max_width=240)
    
    st.write("")
    
    if st.button("✨ 抽一張靜心卡與金句", use_container_width=True):
        if df_cards is not None and df_quotes is not None:
            st.session_state.selected_card = df_cards.sample(1).iloc[0]
            st.session_state.selected_quote = df_quotes.sample(1).iloc[0]
            st.session_state.page = 1
            st.rerun()
        else:
            st.error("請確認 GitHub 已建立 cards.csv 與 quotes.csv")

# ==========================================
# 畫面 2：抽卡結果頁
# ==========================================
elif st.session_state.page == 1:
    card = st.session_state.selected_card
    quote = st.session_state.selected_quote
    card_filename = f"{card['card_id']}.png"
    
    # 顯示圖片
    render_centered_image(card_filename, max_width=240)
    
    # 解析並顯示金句
    if 'quote_text' in quote:
        quote_text = str(quote['quote_text'])
    else:
        quote_text = str(quote.iloc[-1])
        
    st.markdown(f'<div class="quote-box">「 {quote_text} 」</div>', unsafe_allow_html=True)
    
    # DeepSeek API 指引生成
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if api_key:
        with st.spinner("陪伴員正在準備指引..."):
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                context = card.get('prompt_context', '正在觀看這張靜心圖卡')
                
                system_prompt = (
                    "你現在是 333radiance 的靜心陪伴員，風格溫暖、自然、和緩。\n\n"
                    "【輸入資訊】\n"
                    f"- 圖卡意境：{context}\n"
                    f"- 靜心金句：{quote_text}\n\n"
                    "【輸出要求】\n"
                    "1. 內容：結合金句與圖卡意境，給予一句溫柔的呼吸或目光聚焦引導。\n"
                    "2. 字數：嚴格控制在 30 字以內（2-3句話）。\n"
                    "3. 語言規格：必須使用標準繁體中文（書面語）。\n"
                    "4. 禁用詞彙：嚴禁使用任何粵語口語詞（如：唔、睇、望住、咗、嘅、咁）。\n"
                    "5. 語氣：文字平易近人，連 10 歲小孩也能理解與放鬆，不作任何醫療建議。"
                )

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": "請給我一句靜心指示。"}
                    ],
                    max_tokens=80,
                    temperature=0.7
                )
                
                st.success(f"✨ **靜心指引：** {response.choices[0].message.content}")
                
            except Exception as e:
                st.error("系統繁忙中，請深深呼吸，好好照顧自己。")

    # 三按鈕底部選單
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 再抽一次", use_container_width=True):
            st.session_state.page = 0
            st.rerun()
            
    with col2:
        # 安全無跨域問題的 HTML 分享按鈕
        quote_json = json.dumps(quote_text)
        share_html = f"""
        <div style="padding:0; margin:0;">
            <button onclick="shareResult()" style="
                width: 100%;
                padding: 0.45rem 0.2rem;
                border-radius: 18px;
                background-color: #EAD8C8;
                color: #1F1F1F;
                border: none;
                font-family: 'Chiron GoRound TC', sans-serif;
                font-weight: 900;
                font-size: 0.9rem;
                cursor: pointer;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                📤 分享金句
            </button>
        </div>

        <script>
        function shareResult() {{
            const rawQuote = {quote_json};
            const currentUrl = document.referrer || "https://333radiance.streamlit.app/";
            const textToShare = "✨ 333radiance 靜心金句：\\n「" + rawQuote + "」\\n\\n來抽一張你的靜心卡：\\n" + currentUrl;

            if (navigator.share) {{
                navigator.share({{
                    title: '333radiance 靜心空間',
                    text: textToShare,
                    url: currentUrl
                }}).catch(function(e){{}});
            }} else {{
                const dummy = document.createElement("textarea");
                document.body.appendChild(dummy);
                dummy.value = textToShare;
                dummy.select();
                document.execCommand("copy");
                document.body.removeChild(dummy);
                alert("金句與連結已複製！可以貼上至 IG 或訊息分享。");
            }}
        }}
        </script>
        """
        components.html(share_html, height=42)
            
    with col3:
        st.link_button("👉 探索 IG", "https://www.instagram.com/333radiance/", use_container_width=True)

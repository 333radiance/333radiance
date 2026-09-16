import streamlit.components.v1 as components

# 在抽卡結果頁（page 1）底部替換或新增以下程式碼：
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 再抽一次", use_container_width=True):
        st.session_state.page = 0
        st.rerun()

with col2:
    # 建立原生分享按鈕（自動複製金句並喚起手機分享）
    share_html = f"""
    <button onclick="shareResult()" style="
        width: 100%;
        padding: 0.5rem 0.5rem;
        border-radius: 18px;
        background-color: #EAD8C8;
        color: #1F1F1F;
        border: none;
        font-family: 'Chiron GoRound TC', sans-serif;
        font-weight: 900;
        font-size: 0.95rem;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
        📤 分享金句
    </button>

    <script>
    function shareResult() {{
        const textToShare = "✨ 333radiance 靜心金句：\\n「{quote_text}」\\n\\n來抽一張你的靜心卡：";
        const urlToShare = window.parent.location.href;

        if (navigator.share) {{
            navigator.share({{
                title: '333radiance 靜心空間',
                text: textToShare,
                url: urlToShare
            }}).catch((err) => console.log('分享取消', err));
        }} else {{
            navigator.clipboard.writeText(textToShare + " " + urlToShare);
            alert('金句與連結已複製，可直接貼上至 IG 或訊息！');
        }}
    }}
    </script>
    """
    components.html(share_html, height=45)

with col3:
    st.link_button("👉 探索 IG", "https://www.instagram.com/333radiance/", use_container_width=True)

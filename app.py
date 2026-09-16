import streamlit.components.v1 as components

# ... 前面 DeepSeek API 呼叫 ...
# quote_text = response.choices[0].message.content
# st.success(f"✨ **靜心指引：** {quote_text}")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 再抽一次", use_container_width=True):
        st.session_state.page = 0
        st.rerun()

with col2:
    # 將換行符號 \n 轉換為 HTML 的 <br> 以確保分享格式正確
    safe_quote = quote_text.replace('"', '\\"').replace("\n", " ")
    
    share_html = f"""
    <button onclick="shareResult()" style="
        width: 100%;
        padding: 0.55rem 0.5rem;
        border-radius: 20px;
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
        const textToShare = "✨ 333radiance 靜心金句：\\n「{safe_quote}」\\n\\n來抽一張你的靜心卡：";
        const urlToShare = window.parent.location.href;

        if (navigator.share) {{
            navigator.share({{
                title: '333radiance 靜心空間',
                text: textToShare,
                url: urlToShare
            }}).catch((err) => console.log('分享取消', err));
        }} else {{
            // 使用 try-catch 避免部分瀏覽器不支援 clipboard 而報錯
            try {{
                navigator.clipboard.writeText(textToShare + " " + urlToShare).then(() => {{
                    alert('金句與連結已複製，可直接貼上至 IG 或訊息！');
                }});
            }} catch (err) {{
                alert('您的瀏覽器不支援自動複製，請手動選取文字。');
            }}
        }}
    }}
    </script>
    """
    components.html(share_html, height=55)

with col3:
    st.link_button("👉 探索 IG", "https://www.instagram.com/333radiance/", use_container_width=True)

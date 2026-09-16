import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="333radiance 靜心空間", page_icon="✨", layout="centered")

st.title("✨ 333radiance 靜心陪伴空間")
st.write("此刻，請根據你內心的感受，選擇一個最貼近你的狀態：")

api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("輸入 DeepSeek API Key", type="password")

# 圖片路徑已更新為跟你的 GitHub 檔案結構一致
NEEDS_CONFIG = {
    "疲累（需要休息）": {
        "image": "tired.png",
        "description": "觀看流暢的波浪圖卡",
        "prompt_context": "正在觀看一張波浪圖卡，感到疲累需要休息"
    },
    "焦慮（需要平靜）": {
        "image": "anxious.png",
        "description": "觀看幾何同心圓圖卡",
        "prompt_context": "正在觀看一張幾何同心圓圖卡，感到焦慮需要平靜"
    },
    "迷惘（需要方向）": {
        "image": "lost.png",
        "description": "觀看發芽植物與光芒圖卡",
        "prompt_context": "正在觀看一張發芽植物圖卡，感到迷惘需要方向"
    },
    "失眠（需要安心）": {
        "image": "insomnia.png",
        "description": "觀看月亮與夜空圖卡",
        "prompt_context": "正在觀看一張月亮夜空圖卡，失眠難以入睡需要安心"
    }
}

col1, col2 = st.columns(2)
selected_need = None

with col1:
    if st.button("🌊 感到疲累"):
        selected_need = "疲累（需要休息）"
    if st.button("🌱 感到迷惘"):
        selected_need = "迷惘（需要方向）"

with col2:
    if st.button("☸️ 感到焦慮"):
        selected_need = "焦慮（需要平靜）"
    if st.button("🌙 夜晚失眠"):
        selected_need = "失眠（需要安心）"

if selected_need:
    config = NEEDS_CONFIG[selected_need]
    st.divider()

    if os.path.exists(config["image"]):
        st.image(config["image"], caption=config["description"], use_container_width=True)
    else:
        st.warning(f"請確保圖片已上傳至：{config['image']}")

    if not api_key:
        st.info("💡 請設定 DeepSeek API Key 以啟動 AI 靜心陪伴。")
    else:
        with st.spinner("333radiance 靜心陪伴員正在為你準備引導..."):
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.deepseek.com"
                )

                system_prompt = (
                    "你現在是 333radiance 的靜心陪伴員。"
                    f"使用者現在{config['prompt_context']}。"
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
                st.error(f"API 呼叫失敗：{str(e)}")

    st.divider()
    
    st.subheader("🛍️ 5 分鐘線下靜心儀式與實體工具")
    st.write("想配合實體工具，讓心靈得到深層放鬆？")
    st.markdown("[👉 探索 333radiance ](https://www.instagram.com/333radiance/)")

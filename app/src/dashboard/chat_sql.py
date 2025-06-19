def main():
    import streamlit as st
    import pandas as pd
    from openai import OpenAI
    from data.DataConn import db
    import os

    st.title("数据库智能问答机器人（DeepSeek LLM）")

    # 聊天历史
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 读取数据库结构作为system prompt
    db_schema_path = os.path.join(os.path.dirname(__file__), '../data/database.md')
    with open(db_schema_path, encoding='utf-8') as f:
        db_schema = f.read()

    # DeepSeek LLM API配置
    client = OpenAI(api_key="sk-15fb1a6a2f5d4ca1b20b8297c49c99b8", base_url="https://api.deepseek.com")

    def call_llm(messages, model="deepseek-chat"):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content.strip()

    # 聊天输入
    user_input = st.text_input("请输入你的问题：", key="chat_input")
    if st.button("发送") and user_input.strip():
        # 1. 用户消息加入历史
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # 2. 组装 LLM API 输入，生成SQL
        messages = [
            {"role": "system", "content": f"你是一个SQL专家，帮我根据用户问题和数据库结构生成MySQL SQL语句，只返回plain text可以直接进入mysql的SQL而不是markdown格式，不要解释。数据库结构如下：\n{db_schema}"}
        ]
        for msg in st.session_state.chat_history:
            messages.append(msg)
        sql = call_llm(messages)
        st.session_state.chat_history.append({"role": "assistant", "content": f"生成SQL: {sql}"})

        # 3. 执行SQL
        try:
            result_df = db.execute_query_df(sql)
            result_text = result_df.to_markdown(index=False) if not result_df.empty else "无结果"
        except Exception as e:
            result_text = f"SQL执行出错: {e}"

        
        st.session_state.chat_history.append({"role": "assistant", "content": result_text})

    # 聊天历史展示
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**你：** {msg['content']}")
        else:
            st.markdown(f"**机器人：** {msg['content']}")

if __name__ == "__main__":
    main() 
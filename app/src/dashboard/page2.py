import pexpect
import time

def main():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from datetime import datetime, timedelta
    from data.DataLoader import DataLoader

    st.title("用户")
    st.markdown("""
    用户兴趣变化 采用箱线图，前端传给用户每天点击每个category的数量，前端图表显示 每天是一个100%堆柱子，每天柱子的大小不变，然后柱子被每个category按照比例分配大小，唯一的category对应唯一的颜色，点击分析按钮会进行分析、推荐。
    """)

    # 用户ID输入与确认逻辑
    user_id = st.text_input("请输入用户ID：", key="user_id_input")
    if st.button("确认"):
        st.session_state['user_id_confirmed'] = user_id

    confirmed_id = st.session_state.get('user_id_confirmed', None)
    if confirmed_id:
        # 用DataLoader查询用户兴趣分布数据
        loader = DataLoader()
        df = loader.get_user_interest_distribution(confirmed_id)
        if df.empty:
            st.warning(f"用户 {confirmed_id} 暂无兴趣分布数据")
        else:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            df_total = df.groupby('date')['clicks'].transform('sum')
            df['ratio'] = df['clicks'] / df_total

            # 画100%堆叠柱状图
            fig = px.bar(
                df,
                x='date',
                y='ratio',
                color='category',
                title=f'用户 {confirmed_id} 每日各类别点击占比（100%堆叠柱状图）',
                labels={'date': '日期', 'ratio': '占比', 'category': '类别'},
                text_auto='.0%',
            )
            fig.update_layout(barmode='stack', yaxis=dict(tickformat='.0%'))
            st.plotly_chart(fig, use_container_width=True)

        # 分析按钮
        if st.button('分析', key='analyze_btn'):
            # 获取用户兴趣分布数据和历史记录
            interest_df = df.copy()
            history_df = loader.get_user_news_history(confirmed_id, limit=10)
            # 构造prompt，包含用户兴趣分布、历史、数据库结构
            prompt = f"""
你是一个BI分析助手。请基于如下用户兴趣分布数据、历史记录和数据库结构，直接从数据库查询并给出该用户的兴趣分析和内容推荐，要求只输出最终分析和推荐内容，且用markdown格式输出，不要输出任何日志或中间过程。

用户兴趣分布：
{interest_df.to_markdown(index=False)}

历史记录：
{history_df.to_markdown(index=False) if not history_df.empty else '无'}

数据库结构：
- user_behavior_0613_0617(user_id, news_id, category, click_timestamp)
- news_metadata(news_id, title, category, topic, publish_time, content)
"""
            result = ask_openmanus(prompt)
            st.markdown(result)

        # 用户浏览新闻历史（用DataLoader接口）
        st.subheader(f"用户 {confirmed_id} 浏览新闻历史记录")
        history_df = loader.get_user_news_history(confirmed_id, limit=10)
        if not history_df.empty:
            st.dataframe(history_df.drop(columns=['content'], errors='ignore'), use_container_width=True)
        else:
            st.info(f"用户 {confirmed_id} 暂无浏览历史记录")
    else:
        st.info("请输入用户ID并点击确认，查看该用户的兴趣分布和浏览历史。")

def ask_openmanus(user_input: str) -> str:
    try:
        child = pexpect.spawn(
            'python /home/Lyunzh/文档/BI/BI_Final/app/OpenManus/main.py',
            encoding='utf-8',
            timeout=180
        )
        child.expect('Enter your prompt:')
        child.sendline(user_input)
        time.sleep(120)  # 等待2分钟
        output = child.read()  # 捕获所有输出
        child.close()
        return output.strip() if output.strip() else '未检测到OpenManus输出，请检查运行情况。'
    except Exception as e:
        return f"OpenManus调用失败: {e}"

if __name__ == "__main__":
    main() 
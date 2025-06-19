def main():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from datetime import datetime, timedelta

    st.title("第二个页面")
    st.markdown("""
    用户兴趣变化 采用箱线图，前端传给用户每天点击每个category的数量，前端图表显示 每天是一个100%堆柱子，每天柱子的大小不变，然后柱子被每个category按照比例分配大小，唯一的category对应唯一的颜色，点击分析按钮会进行分析、推荐。
    """)

    # 用户ID输入与确认逻辑
    user_id = st.text_input("请输入用户ID：", key="user_id_input")
    if st.button("确认"):
        st.session_state['user_id_confirmed'] = user_id

    confirmed_id = st.session_state.get('user_id_confirmed', None)
    if confirmed_id:
        # 写死的用户兴趣分布数据
        categories = ['科技', '娱乐', '体育', '财经']
        dates = pd.date_range(start='2024-01-01', end='2024-01-07', freq='D')
        data = []
        for date in dates:
            total = 1000
            values = [
                int(total * 0.2 + (i * 10 + date.day * 5) % 100) for i in range(len(categories))
            ]
            values = [v if v > 0 else 10 for v in values]
            for cat, val in zip(categories, values):
                data.append({'date': date, 'category': cat, 'clicks': val})
        df = pd.DataFrame(data)

        # 计算每天总点击量和每个category的比例
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
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
            st.success(f"用户 {confirmed_id} 本周对体育和科技类内容兴趣较高，建议加强相关内容推送。")

        # 用户浏览新闻历史（写死数据）
        st.subheader(f"用户 {confirmed_id} 浏览新闻历史记录")
        history_data = []
        for i in range(1, 11):
            cat = categories[i % 4]
            topic = f"{cat}话题{i}"
            history_data.append({
                'newsid': 1000 + i,
                'category': cat,
                'topic': topic,
                'title': f"{cat} - {topic} 新闻标题",
                'content': f"{cat}领域关于{topic}的新闻内容...",
                'view_time': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M'),
                'hot': 100 + i * 5
            })
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df.drop(columns=['content', 'hot']), use_container_width=True)

    else:
        st.info("请输入用户ID并点击确认，查看该用户的兴趣分布和浏览历史。")

if __name__ == "__main__":
    main() 
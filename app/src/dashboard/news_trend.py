def main():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from data.DataLoader import DataLoader

    st.title("新闻点击趋势与相似新闻推荐")
    news_id = st.text_input("请输入新闻ID：")
    if not news_id:
        st.info("请输入新闻ID以查询该新闻的点击趋势和相似新闻。")
        return

    loader = DataLoader()

    # 查询该新闻每天的点击次数
    df = loader.get_news_lifecycle(news_id)
    if df.empty:
        st.warning("未查询到该新闻的点击趋势数据。")
    else:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        fig = px.bar(df, x='date', y='clicks', title=f'新闻 {news_id} 每日点击次数', labels={'date': '日期', 'clicks': '点击次数'})
        st.plotly_chart(fig, use_container_width=True)

    # 查询该新闻的topic
    topic = loader.get_news_topic(news_id)
    if not topic:
        st.warning("未查询到该新闻的topic，无法推荐相似新闻。")
        return
    st.info(f"该新闻的topic为：{topic}")

    # 查询相同topic的10条新闻（排除自身）
    sim_df = loader.get_similar_news_by_topic(topic, news_id, limit=10)
    st.subheader("相同topic的10条新闻推荐")
    if sim_df.empty:
        st.info("暂无相同topic的新闻推荐。")
    else:
        for idx, row in sim_df.iterrows():
            with st.expander(f"{row['title']} | {row['news_id']} | {row['category']} | {row['topic']}"):
                st.write(row['content'])

if __name__ == "__main__":
    main() 
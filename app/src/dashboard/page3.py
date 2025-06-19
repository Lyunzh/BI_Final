def main():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from data.DataLoader import DataLoader

    st.title("最近一天新闻分布（饼状图）")
    st.markdown("""
    - 展示最近一天的新闻，饼状图显示每个category的分类。
    - 鼠标悬停到每个category扇区时，显示top5（如有）热点topic。
    """)

    loader = DataLoader()
    latest_date = loader.get_latest_date()
    st.info(f"最近一天（数据库最新行为日期）为：{latest_date}")

    # 查询最近一天新闻数据
    df = loader.get_latest_news(latest_date)
    if df.empty:
        st.warning("暂无新闻数据")
        return

    # 统计每个category的新闻条数
    cat_count = df.groupby('category').size().reset_index(name='count')

    # 生成每个category的top5 topic字符串
    def get_top5_topics(x):
        top5 = x.groupby('topic').size().sort_values(ascending=False).head(5)
        return '\n'.join([f"{i+1}. {topic}" for i, topic in enumerate(top5.index)])
    top_topics = df.groupby('category').apply(get_top5_topics).to_dict()
    cat_count['top5'] = cat_count['category'].map(top_topics)

    # 画饼图
    fig = px.pie(
        cat_count,
        names='category',
        values='count',
        title='最近一天新闻各类别分布',
        hole=0.3
    )
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>新闻数: %{value}<br>Top5热点:\n%{customdata[0]}',
        customdata=cat_count[['top5']].values
    )

    st.plotly_chart(fig, use_container_width=True)

    # 展示最火的10个新闻（expander样式）
    st.subheader("最火的10个新闻")
    df_top10 = loader.get_top10_news_per_day(latest_date)
    if not df_top10.empty:
        for idx, row in df_top10.iterrows():
            with st.expander(f"{row['title']} | {row['news_id']} | {row['category']} | {row['topic']} | 热度: {row['clicks']}"):
                st.write(row['content'])
    else:
        st.info("暂无数据")

if __name__ == "__main__":
    main() 
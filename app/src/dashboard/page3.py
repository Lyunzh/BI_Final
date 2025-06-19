def main():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from datetime import datetime, timedelta
    import random

    st.title("最近一天新闻分布（饼状图）")
    st.markdown("""
    - 展示最近一天的新闻，饼状图显示每个category的分类。
    - 鼠标悬停到每个category扇区时，显示top5（如有）热点topic。
    """)

    # 写死的最近一天新闻数据
    categories = ['科技', '娱乐', '体育', '财经']
    topics = {
        '科技': ['AI突破', '量子计算', '元宇宙', '芯片升级', '自动驾驶', '云计算', '大数据'],
        '娱乐': ['新电影', '明星八卦', '音乐节', '综艺首播', '颁奖典礼'],
        '体育': ['世界杯', 'NBA', '奥运会', '马拉松', '网球公开赛'],
        '财经': ['股市大涨', '央行政策', '企业并购', '基金热销', '数字货币']
    }
    news_data = []
    today = datetime.now().date()
    news_id = 1
    for cat in categories:
        topic_list = random.sample(topics[cat], k=min(5, len(topics[cat])))
        for topic in topic_list:
            news_data.append({
                'newsid': news_id,
                'date': today,
                'category': cat,
                'topic': topic,
                'title': f"{cat} - {topic} 重大新闻",
                'content': f"{cat}领域关于{topic}的最新进展和深度报道内容...",
                'hot': random.randint(50, 200)
            })
            news_id += 1
    df = pd.DataFrame(news_data)

    # 统计每个category的新闻条数
    cat_count = df.groupby('category').size().reset_index(name='count')

    # 生成每个category的top5 topic字符串
    top_topics = (
        df.groupby('category')
        .apply(lambda x: '\n'.join([f"{i+1}. {row['topic']} (热度{row['hot']})" for i, row in x.nlargest(5, 'hot').iterrows()]))
        .to_dict()
    )
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
    top10_news = df.nlargest(10, 'hot')[['newsid', 'category', 'topic', 'title', 'content', 'hot']]
    for idx, row in top10_news.iterrows():
        with st.expander(f"{row['title']} | {row['newsid']} | {row['category']} | {row['topic']} | 热度: {row['hot']}"):
            st.write(row['content'])

if __name__ == "__main__":
    main() 
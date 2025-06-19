def main():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    from datetime import datetime, timedelta
    import random
    import os


    # 模拟新闻数据
    def get_news_by_topic_and_time(topic, time):
        news_data = {
            'AI技术突破': [
                {'title': 'OpenAI发布GPT-5', 'content': 'OpenAI今日宣布发布新一代AI模型GPT-5...', 'hot': 95},
                {'title': 'AI在医疗领域取得重大突破', 'content': '最新AI诊断系统准确率达到98%...', 'hot': 88},
                {'title': '量子AI研究新进展', 'content': '科学家在量子计算与AI结合方面取得突破...', 'hot': 85}
            ],
            '新电影上映': [
                {'title': '《流浪地球3》首映', 'content': '科幻巨制《流浪地球3》今日全国首映...', 'hot': 92},
                {'title': '《复仇者联盟6》预告片发布', 'content': '漫威新作《复仇者联盟6》预告片引发热议...', 'hot': 90},
                {'title': '《泰坦尼克号》重映', 'content': '经典电影《泰坦尼克号》4K重制版上映...', 'hot': 87}
            ],
            '世界杯预选赛': [
                {'title': '中国队2:0战胜韩国队', 'content': '世界杯预选赛亚洲区，中国队主场2:0战胜韩国队...', 'hot': 96},
                {'title': '梅西确认参加2026世界杯', 'content': '阿根廷球星梅西确认将参加2026年世界杯...', 'hot': 94},
                {'title': '世界杯预选赛赛程公布', 'content': '2026年世界杯预选赛完整赛程公布...', 'hot': 89}
            ],
            '股市大涨': [
                {'title': '上证指数突破4000点', 'content': '今日上证指数突破4000点大关，创历史新高...', 'hot': 93},
                {'title': '科技股领涨大盘', 'content': '科技板块今日领涨，多只个股涨停...', 'hot': 91},
                {'title': '央行降准利好股市', 'content': '央行宣布降准0.5个百分点，市场反应积极...', 'hot': 88}
            ]
        }
        
        if topic in news_data:
            return sorted(news_data[topic], key=lambda x: x['hot'], reverse=True)
        return []

    # 生成模拟数据
    def generate_mock_data():
        categories = ['科技', '娱乐', '体育', '财经']
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        
        data = []
        for category in categories:
            for date in dates:
                click_times = random.randint(100, 1000)
                hot_topics = {
                    '科技': ['AI技术突破', '量子计算新进展', '元宇宙发展'],
                    '娱乐': ['新电影上映', '明星八卦', '音乐盛典'],
                    '体育': ['世界杯预选赛', 'NBA季后赛', '奥运会筹备'],
                    '财经': ['股市大涨', '央行政策', '企业并购']
                }
                data.append({
                    'category': category,
                    'time': date,
                    'click_times': click_times,
                    'hotest_topic': random.choice(hot_topics[category])
                })
        
        return pd.DataFrame(data)

    # 生成数据
    df = generate_mock_data()

    # 创建标题
    st.title("类别趋势分析仪表板")

    # 用户选择类别
    selected_category = st.selectbox("选择类别进行高峰分析", df['category'].unique())

    # 分析函数：返回该类别的高峰点和分析文本
    def fake_analysis(category, df):
        sub_df = df[df['category'] == category]
        max_row = sub_df.loc[sub_df['click_times'].idxmax()]
        analysis_text = f"{category}在{max_row['time'].strftime('%Y-%m-%d')}达到点击高峰（{max_row['click_times']}次），可能由于重大事件或新闻引发关注。"
        return {
            'time': max_row['time'],
            'click_times': max_row['click_times'],
            'text': analysis_text
        }

    analysis_result = fake_analysis(selected_category, df)

    # 创建折线图
    fig = px.line(df, 
                  x='time', 
                  y='click_times', 
                  color='category',
                  title='各类别点击量趋势',
                  labels={'time': '时间', 'click_times': '点击次数', 'category': '类别'})

    # 添加悬停信息
    fig.update_traces(
        hovertemplate="<br>".join([
            "时间: %{x}",
            "点击次数: %{y}",
            "类别: %{customdata[0]}",
            "热门话题: %{customdata[1]}"
        ]),
        customdata=df[['category', 'hotest_topic']].values
    )

    # 为选中类别的高峰点添加注释
    fig.add_annotation(
        x=analysis_result['time'],
        y=analysis_result['click_times'],
        text=analysis_result['text'],
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-80,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='red',
        font=dict(color='black'),
        arrowcolor='red',
        borderpad=4
    )

    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

    # 添加新闻展示区域
    st.subheader("热门新闻")
    selected_topic = st.selectbox(
        "选择热门话题",
        options=sorted(set(df['hotest_topic'].unique()))
    )

    if selected_topic:
        news_list = get_news_by_topic_and_time(selected_topic, datetime.now())
        for news in news_list:
            with st.expander(f"{news['title']} (热度: {news['hot']})"):
                st.write(news['content'])

    # 添加交互式新闻展示
    st.subheader("实时新闻")
    hover_data = st.session_state.get('hover_data', None)
    if hover_data:
        time = hover_data.get('time')
        category = hover_data.get('category')
        topic = hover_data.get('topic')
        
        st.write(f"时间: {time}")
        st.write(f"类别: {category}")
        st.write(f"热门话题: {topic}")
        
        news_list = get_news_by_topic_and_time(topic, time)
        for news in news_list:
            with st.expander(f"{news['title']} (热度: {news['hot']})"):
                st.write(news['content'])

    # 添加JavaScript代码来处理悬停事件
    st.markdown("""
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const plot = document.querySelector('.js-plotly-plot');
            plot.on('plotly_hover', function(data) {
                const point = data.points[0];
                const time = point.x;
                const category = point.customdata[0];
                const topic = point.customdata[1];
                
                // 发送数据到Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: {
                        time: time,
                        category: category,
                        topic: topic
                    }
                }, '*');
            });
        });
    </script>
    """, unsafe_allow_html=True)

    st.title("查询日志查看")

    log_path = os.path.join(os.path.dirname(__file__), '../log/query_log.csv')
    log_path = os.path.abspath(log_path)

    if not os.path.exists(log_path):
        st.warning("日志文件不存在。")
    else:
        df = pd.read_csv(log_path)
        if not df.empty:
            # 按照timestamp倒序排列
            df = df.sort_values(by='timestamp', ascending=False).reset_index(drop=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("日志文件为空。")

if __name__ == "__main__":
    main() 
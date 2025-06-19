def main():
    import streamlit as st
    from data.DataLoader import DataLoader
    import plotly.express as px

    st.title("类别趋势分析仪表板")
    loader = DataLoader()
    latest_date = loader.get_latest_date()
    st.info(f"最近一天（数据库最新行为日期）为：{latest_date}")

    # 查询类别趋势数据
    df = loader.get_category_daily_hot()
    if df.empty:
        st.warning("暂无类别趋势数据")
        return

    # 类别选择
    categories = sorted(df['category'].unique())
    selected_category = st.selectbox("选择类别进行高峰分析", categories)

    # 计算高峰点
    sub_df = df[df['category'] == selected_category]
    if sub_df.empty:
        st.warning(f"{selected_category} 暂无数据")
        return
    max_row = sub_df.loc[sub_df['clicks'].idxmax()]
    analysis_text = f"{selected_category}在{max_row['date']}达到点击高峰（{max_row['clicks']}次），可能由于重大事件或新闻引发关注。"

    # 画折线图
    fig = px.line(df, x='date', y='clicks', color='category',
                  title='各类别点击量趋势',
                  labels={'date': '时间', 'clicks': '点击次数', 'category': '类别'})
    fig.add_annotation(
        x=max_row['date'],
        y=max_row['clicks'],
        text=analysis_text,
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
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main() 
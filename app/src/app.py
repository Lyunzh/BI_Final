import streamlit as st
from dashboard import main, page2, page3, log_view, news_trend, chat_sql

st.set_page_config(page_title="BI Dashboard", layout="wide")
st.sidebar.title("页面导航")
page = st.sidebar.radio("请选择页面", ["首页", "用户", "新闻饼状图页面", "日志查看", "新闻趋势与推荐", "数据库智能问答"])

if page == "首页":
    main.main()
elif page == "用户":
    page2.main()
elif page == "新闻饼状图页面":
    page3.main()
elif page == "日志查看":
    log_view.main()
elif page == "新闻趋势与推荐":
    news_trend.main()
elif page == "数据库智能问答":
    chat_sql.main()

import streamlit as st
st.set_page_config(page_title="BI Dashboard", layout="wide")
import app
import page2
import page3
import log_view

st.sidebar.title("页面导航")
page = st.sidebar.radio("请选择页面", ["首页", "第二个页面", "新闻饼状图页面", "日志查看"])

if page == "首页":
    app.main()
elif page == "第二个页面":
    page2.main()
elif page == "新闻饼状图页面":
    page3.main()
elif page == "日志查看":
    log_view.main() 
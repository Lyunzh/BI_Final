import streamlit as st
import pandas as pd
import os

def main():
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
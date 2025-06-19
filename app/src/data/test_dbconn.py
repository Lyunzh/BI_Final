from DataConn import db

def main():
    # 测试简单查询
    try:
        df = db.execute_query_df("SELECT 1 as test_col")
        print("查询结果：")
        print(df)
        print("数据库连接和查询正常！")
    except Exception as e:
        print("数据库连接或查询失败：", e)

if __name__ == "__main__":
    main()
from  data.DataConn import db
import pandas as pd
from typing import Optional


class DataLoader:
    
    def __init__(self, use_sample_data: Optional[bool] = None):
        self._news_cache=None
        
    def load_news_cycle(self, news_id : str)->pd.DataFrame:
        try:
            pass
        except Exception as e:
            logger.error(f"Error loading data from database: {str(e)}")
        
        return pd.DataFrame()
        
    def load_category_cycle(self)->pd.DataFrame:
                
        pass
    
    
    def clear_cache(self):
        pass

    def get_latest_date(self) -> str:
        """
        获取 user_behavior_0613_0617 表中最新一条记录的日期（YYYY-MM-DD）
        """
        query = "SELECT MAX(event_time) as latest_time FROM user_behavior_0613_0617"
        df = db.execute_query_df(query)
        if not df.empty and pd.notnull(df.iloc[0]['latest_time']):
            return pd.to_datetime(df.iloc[0]['latest_time']).strftime('%Y-%m-%d')
        else:
            return pd.Timestamp.now().strftime('%Y-%m-%d')

    def get_user_interest_distribution(self, user_id: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        date_filter = ""
        params = {"user_id": user_id}
        if start_date:
            date_filter += " AND ub.event_time >= %(start_date)s"
            params["start_date"] = start_date
        if end_date:
            date_filter += " AND ub.event_time <= %(end_date)s"
            params["end_date"] = end_date
        query = f'''
            SELECT DATE(ub.event_time) as date, nm.category, COUNT(*) as clicks
            FROM user_behavior_0613_0617 ub
            JOIN news_metadata nm ON ub.news_id = nm.news_id
            WHERE ub.user_id = %(user_id)s {date_filter}
            GROUP BY DATE(ub.event_time), nm.category
            ORDER BY date, nm.category
        '''
        return db.execute_query_df(query, params)

    def get_user_news_history(self, user_id: str, limit: int = 20) -> pd.DataFrame:
        query = '''
            SELECT ub.event_time, ub.news_id, nm.title, nm.category, nm.topic, nm.content, ub.duration
            FROM user_behavior_0613_0617 ub
            JOIN news_metadata nm ON ub.news_id = nm.news_id
            WHERE ub.user_id = %(user_id)s
            ORDER BY ub.event_time DESC
            LIMIT %(limit)s
        '''
        params = {"user_id": user_id, "limit": limit}
        return db.execute_query_df(query, params)

    def get_latest_news(self, date: str = None) -> pd.DataFrame:
        if date is None:
            date = self.get_latest_date()
        query = '''
            SELECT news_id, title, category, topic, content, create_time
            FROM news_metadata
            WHERE DATE(create_time) = %(date)s
            ORDER BY create_time DESC
        '''
        params = {"date": date}
        return db.execute_query_df(query, params)

    def get_hottest_topic_per_category(self, date: str = None) -> pd.DataFrame:
        if date is None:
            date = self.get_latest_date()
        query = '''
            SELECT nm.category, nm.topic, COUNT(*) as clicks
            FROM user_behavior_0613_0617 ub
            JOIN news_metadata nm ON ub.news_id = nm.news_id
            WHERE DATE(ub.event_time) = %(date)s
            GROUP BY nm.category, nm.topic
            ORDER BY nm.category, clicks DESC
        '''
        params = {"date": date}
        df = db.execute_query_df(query, params)
        return df.sort_values(['category', 'clicks'], ascending=[True, False]).groupby('category').head(1).reset_index(drop=True)

    def get_top10_news_per_day(self, date: str = None) -> pd.DataFrame:
        if date is None:
            date = self.get_latest_date()
        query = '''
            SELECT nm.news_id, nm.title, nm.category, nm.topic, nm.content, COUNT(*) as clicks
            FROM user_behavior_0613_0617 ub
            JOIN news_metadata nm ON ub.news_id = nm.news_id
            WHERE DATE(ub.event_time) = %(date)s
            GROUP BY nm.news_id, nm.title, nm.category, nm.topic, nm.content
            ORDER BY clicks DESC
            LIMIT 10
        '''
        params = {"date": date}
        return db.execute_query_df(query, params)

    def get_category_daily_hot(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        date_filter = ""
        params = {}
        if start_date:
            date_filter += " AND ub.event_time >= %(start_date)s"
            params["start_date"] = start_date
        if end_date:
            date_filter += " AND ub.event_time <= %(end_date)s"
            params["end_date"] = end_date
        query = f'''
            SELECT DATE(ub.event_time) as date, nm.category, COUNT(*) as clicks
            FROM user_behavior_0613_0617 ub
            JOIN news_metadata nm ON ub.news_id = nm.news_id
            WHERE 1=1 {date_filter}
            GROUP BY DATE(ub.event_time), nm.category
            ORDER BY date, nm.category
        '''
        return db.execute_query_df(query, params)

    def get_news_lifecycle(self, news_id: str) -> pd.DataFrame:
        """
        查询某新闻每天的点击次数
        返回DataFrame: columns=['date', 'clicks']
        """
        query = '''
            SELECT DATE(ub.event_time) as date, COUNT(*) as clicks
            FROM user_behavior_0613_0617 ub
            WHERE ub.news_id = %(news_id)s
            GROUP BY DATE(ub.event_time)
            ORDER BY date
        '''
        params = {"news_id": news_id}
        return db.execute_query_df(query, params)

    def get_news_topic(self, news_id: str) -> Optional[str]:
        query = 'SELECT topic FROM news_metadata WHERE news_id = %(news_id)s'
        params = {"news_id": news_id}
        df = db.execute_query_df(query, params)
        if not df.empty and pd.notnull(df.iloc[0]['topic']):
            return df.iloc[0]['topic']
        return None

    def get_similar_news_by_topic(self, topic: str, news_id: str, limit: int = 10) -> pd.DataFrame:
        query = '''
            SELECT news_id, title, category, topic, content, create_time
            FROM news_metadata
            WHERE topic = %(topic)s AND news_id != %(news_id)s
            ORDER BY create_time DESC
            LIMIT %(limit)s
        '''
        params = {"topic": topic, "news_id": news_id, "limit": limit}
        return db.execute_query_df(query, params)
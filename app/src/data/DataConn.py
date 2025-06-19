import logging
import pandas as pd
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
from datetime import datetime


logger = logging.getLogger(__name__)
def log_query(query: str, elapsed: float, log_path='~/文档/BI/BI_Final/app/src/log/query_log.csv'):
    log_entry = {
        'query': query,
        'elapsed_seconds': elapsed,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    df_log = pd.DataFrame([log_entry])
    if not os.path.exists(log_path):
        df_log.to_csv(log_path, index=False)
    else:
        df_log.to_csv(log_path, mode='a', header=False, index=False)

class DBConn:
    def __init__(self):
        self.engine: Optional[Engine] = None
        self.max_retries = 3
        self.retry_delay = 1  # Initial delay in seconds

    def connect(self) -> bool:
        for attempt in range(self.max_retries):
            try:
                user = "root"
                password = "Tongjidb"
                host = "127.0.0.1"
                port = "3306"
                db_name = "pens"
                # 推荐用pymysql
                connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
                self.engine = create_engine(
                    connection_string,
                    poolclass=QueuePool,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=1800
                )
                # 测试连接
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info(f"Successfully connected to MySQL {host}:{port}/{db_name}")
                return True
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
                self.engine = None
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.info(f"Retrying connection in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retry attempts reached. Could not establish database connection.")
                    return False
        return False

    def disconnect(self) -> None:
        if self.engine:
            try:
                self.engine.dispose()
            except:
                pass
            self.engine = None
        logger.info("Disconnected from database")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception),
        before_sleep=lambda retry_state: logger.warning(f"Retrying query after error: {retry_state.outcome.exception()}")
    )
    def execute_query_df(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a query and return DataFrame results with retry logic.
        """
        try:
            start_time = time.time()
            if not self.engine:
                if not self.connect():
                    logger.error("Could not establish connection to the database")
                    return pd.DataFrame()
            result = pd.read_sql_query(query, self.engine, params=params)
            elapsed = time.time() - start_time
            log_query(query, elapsed)
            return result
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise

db = DBConn()
db.connect()
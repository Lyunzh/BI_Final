import logging
import pymysql
import pandas as pd
from typing import Dict, Any, List, Optional, Union
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
from datetime import datetime

from utils.config_loader import config
from utils.timer import log

logger = logging.getLogger(__name__)

def log_query(query: str, elapsed: float, log_path='app/src/log/query_log.csv'):
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
        self.db_config = config.get_database_config()
        self.connection = None
        self.engine = None
        self.max_retries = 3
        self.retry_delay = 1  # Initial delay in seconds
        
    def connect(self) -> bool:
        for attempt in range(self.max_retries):
            try:
                # Build connection string
                user = self.db_config.get('user')
                password = self.db_config.get('password')
                host = self.db_config.get('host')
                port = self.db_config.get('port')
                db_name = self.db_config.get('name')
                ssl_mode = self.db_config.get("ssl_mode", "disable")
                
                # Create SQLAlchemy engine with connection pooling
                connection_string = f"mysql://{user}:{password}@{host}:{port}/{db_name}"
                self.engine = create_engine(
                    connection_string,
                    connect_args={"sslmode": ssl_mode},
                    poolclass=QueuePool,
                    pool_size=5,
                    max_overflow=10,
                    pool_timeout=30,
                    pool_recycle=1800  # Recycle connections after 30 minutes
                )
                
                # Also create connection for backwards compatibility
                self.connection = pymysql.connect(
                    connection_string,
                    sslmode=ssl_mode,
                    keepalives=1,
                    keepalives_idle=30,
                    keepalives_interval=10,
                    keepalives_count=5
                )
                
                # Test the connection
                self._test_connection()
                
                logger.info(f"Successfully connected to database {host}:{port}/{db_name}")
                return True
                
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {str(e)}")
                self._cleanup_connections()
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying connection in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error("Max retry attempts reached. Could not establish database connection.")
                    return False
        
        return False
        
    def _test_connection(self) -> None:
        """Test if the database connection is working."""
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
        except Exception as e:
            raise Exception(f"Connection test failed: {str(e)}")
    
    def _cleanup_connections(self) -> None:
        """Clean up existing connections."""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection = None
        if self.engine:
            try:
                self.engine.dispose()
            except:
                pass
            self.engine = None
    
    def disconnect(self) -> None:
        """Disconnect from the database."""
        self._cleanup_connections()
        logger.info("Disconnected from database")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((psycopg2.OperationalError, psycopg2.InterfaceError)),
        before_sleep=lambda retry_state: logger.warning(f"Retrying query after error: {retry_state.outcome.exception()}")
    )
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results with retry logic.
        
        Args:
            query: SQL query statement
            params: Query parameters
            
        Returns:
            List of query results
        """
        result = []
        
        try:
            # Ensure a connection is established
            if not self.connection:
                if not self.connect():
                    logger.error("Could not establish connection to the database")
                    return []
            
            # Verify the connection is valid
            if self.connection is None:
                logger.error("Database connection is invalid")
                return []
                
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or {})
                result = cursor.fetchall()
                
            return [dict(row) for row in result]
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((psycopg2.OperationalError, psycopg2.InterfaceError)),
        before_sleep=lambda retry_state: logger.warning(f"Retrying query after error: {retry_state.outcome.exception()}")
    )
    def execute_query_df(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute a query and return DataFrame results with retry logic.
        
        Args:
            query: SQL query statement
            params: Query parameters
            
        Returns:
            Query results as DataFrame
        """
        try:
            start_time = time.time()
            # Ensure a connection is established
            if not self.engine:
                if not self.connect():
                    logger.error("Could not establish connection to the database")
                    return pd.DataFrame()
            
            # Verify the engine is valid
            if self.engine is None:
                logger.error("Database connection is invalid")
                return pd.DataFrame()
                
            # Use SQLAlchemy engine instead of direct psycopg2 connection
            result = pd.read_sql_query(query, self.engine, params=params)
            elapsed = time.time() - start_time
            log_query(query, elapsed)
            return result
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise  # Re-raise to trigger retry logic
        
        
db = DBConn()
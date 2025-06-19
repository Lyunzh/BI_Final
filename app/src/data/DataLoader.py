from  data.DataConn import db


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
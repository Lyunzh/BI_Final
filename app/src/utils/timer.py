import time
import logging

def log(func):
    def wrapper(*args,**kargs):
        start_time= time.time()
        logging.info("start %s ()" %func.__name__)
        ret=func(*args,**kargs)
        end_time= time.time()
        logging.info("end %s()" %func.__name__)
        logging.info(f"cost {end_time-start_time} seconds")
        return ret
    return wrapper
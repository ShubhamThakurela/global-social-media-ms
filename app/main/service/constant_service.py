import datetime
import time

from app.main.constant import paths


class ConstantService:
    @staticmethod
    def fetched_scraped_data():
        time.sleep(3)
        # return paths.SCRAPPED_PATH + '/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        return paths.SCRAPPED_PATH + '/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

    @staticmethod
    def data_in_path():
        return paths.IN_PATH

    @staticmethod
    def data_processed_path():
        return paths.PROCESSED_PATH

    @staticmethod
    def data_out_path():
        return paths.SCRAPPED_PATH

    @staticmethod
    def log_path():
        return paths.LOG_PATH

    @staticmethod
    def server_host():
        return paths.SERVER_HOST

    @staticmethod
    def get_max_retry():
        return paths.MAX_RETRY

    @staticmethod
    def all_sources():
        return paths.SOURCES

    @staticmethod
    def get_chrome_path():
        return paths.CHROME_PATH
    
    @staticmethod
    def get_user_agent():
        # return proxy.ua.random
        return 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
    
    @staticmethod
    def cc_mail_id():
        return ""
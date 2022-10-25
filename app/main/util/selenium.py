import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from bs4 import BeautifulSoup, Comment
import time
import cv2
import time
# from ..util.captcha import solve_blocked
from ..service.constant_service import ConstantService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc



def get_content(org_url):
    result = None
    retry = ConstantService.get_max_retry()
    while retry > 0 and result is None:
        print(retry)
        result, driver = fetch(org_url)
        retry -= 1
    return result, driver


def fetch(org_url):
    try:
        content = None
        options = webdriver.ChromeOptions()
        # options.add_experimental_option("useAutomationExtension", False)
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options = uc.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--remote-debugging-port=9222')
        # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # # options.add_argument('user-agent={0}'.format(ConstantService.get_user_agent()))
        # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        # driver = uc.Chrome(chrome_options=options)
        # driver = webdriver.Chrome(executable_path=ConstantService.get_chrome_path(), chrome_options=options)

        # options.user_data_dir = r"C:\Users\User\AppData\Local\Google\Chrome\User Data\Default"
        # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        proxies = {
            'http': 'http://scraperapi:9d91348e78da6f75a5167d92db1234b9@proxy-server.scraperapi.com:8001',
        }
        options.add_argument('--proxy-server=%s' % proxies)
        driver = uc.Chrome(options=options)
        driver.get(org_url)
        time.sleep(10)
        content = driver.find_element('xpath', '/html/body')
    except Exception as e:
        print(str(e))
        time.sleep(5)
        return None
    else:
        # driver.close()
        return content, driver






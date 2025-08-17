from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
import sys

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=ko-KR")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("disable-blink-features=AutomationControlled")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

    service = Service(executable_path='/usr/bin/chromedriver')
    return webdriver.Chrome(options=chrome_options, service=service)

def get_with_retry(driver, url, max_retries=3, wait_time=2, timeout=60):
    driver.set_page_load_timeout(timeout)
    for attempt in range(1, max_retries + 1):
        try:
            driver.get(url)
            break
        except TimeoutException as e:
            if attempt == max_retries:
                print("❌ Max retries reached.")
                sys.exit(1)
            print(f"⚠️ Retry {attempt}/{max_retries}: {e}")
            time.sleep(wait_time)

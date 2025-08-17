from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import urllib3
import time

def create_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions") 
    # chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--lang=ko-KR")
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    return webdriver.Chrome(options=chrome_options)

def get_with_retry(driver, url, max_retries=3, wait_time=2, timeout=60):
    driver.set_page_load_timeout(timeout)
    for attempt in range(max_retries):
        try:
            print(f"[attempt {attempt+1}] Trying: {url}")
            driver.get(url)
            print("successfully loaded:", url)
            return
        except (TimeoutException, urllib3.exceptions.ReadTimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retrying after timeout: {e}")
            time.sleep(wait_time)
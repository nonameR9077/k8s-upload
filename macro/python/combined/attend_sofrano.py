from crawler import create_driver, get_with_retry
from utils import try_captcha_attendance
from constants import CREDENTIALS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

CAPTCHA_TRY_COUNT = 7

def attend(headless=True):
    info = CREDENTIALS["sofrano"]
    driver = create_driver(headless)
    try:
        get_with_retry(driver, info["login_url"])
        driver.implicitly_wait(5)

        id_input = driver.find_element(By.XPATH, '//*[@id="member_id"]')
        pw_input = driver.find_element(By.XPATH, '//*[@id="member_passwd"]')

        # pw_input.click()
        pw_input.send_keys(info["password"])

        time.sleep(2)

        # id_input.click()
        id_input.send_keys(info["id"], Keys.RETURN)

        driver.get(info["attendance_url"])
        driver.implicitly_wait(5)
        
        try_captcha_attendance(driver, info["attendance_url"], CAPTCHA_TRY_COUNT)

    except Exception as e:
        print("[sofrano] Error:", e)
        raise e
    finally:
        driver.quit()

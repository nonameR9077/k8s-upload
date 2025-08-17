from crawler import create_driver, get_with_retry
from constants import CREDENTIALS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def attend(headless=True):
    info = CREDENTIALS["herotime"]
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

        driver.execute_script("attend_send('pass');")
        
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("[herotime]", alert.text)
        alert.accept()
    except Exception as e:
        print("[herotime] Error:", e)
        raise e
    finally:
        driver.quit()

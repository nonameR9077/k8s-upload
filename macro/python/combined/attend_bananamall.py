from crawler import create_driver, get_with_retry
from constants import CREDENTIALS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def attend(headless=True):
    info = CREDENTIALS["bananamall"]
    driver = create_driver(headless)
    try:
        get_with_retry(driver, info["login_url"])
        driver.implicitly_wait(5)
        driver.find_element(By.ID, "passwd").send_keys(info["password"])
        time.sleep(1)
        driver.find_element(By.ID, "id").send_keys(info["id"])
        time.sleep(2)

        driver.get(info["attendance_url"])
        driver.implicitly_wait(5)
        
        driver.execute_script("attendance_check();")
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("[bananamall]", alert.text)
        alert.accept()
    except Exception as e:
        print("[bananamall] Error:", e)
        raise e
    finally:
        driver.quit()

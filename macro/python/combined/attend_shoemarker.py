from crawler import create_driver, get_with_retry
from constants import CREDENTIALS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

def attend(headless=True):
    info = CREDENTIALS["shoemarker"]
    driver = create_driver(headless)
    try:
        get_with_retry(driver, info["login_url"])
        driver.implicitly_wait(5)

        id_input = driver.find_element(By.XPATH, '//*[@id="login-id"]')
        pw_input = driver.find_element(By.XPATH, '//*[@id="login-pw"]')

        
        pw_input.send_keys(info["password"])

        # pw_input.click()
        # pw_input.send_keys(info["password"])

        time.sleep(2)

        id_input.send_keys(info["id"], Keys.RETURN)

        # id_input.click()
        # id_input.send_keys(info["id"])


        # give 3 likes
        click_3_likes(driver, info["main_url"])

        driver.get(info["attendance_url"])
        driver.implicitly_wait(5)

        driver.execute_script("attendOk();")

        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("[shoemarker]", alert.text)
        alert.accept()

        # ungive 3 likes
        click_3_likes(driver, info["main_url"])

    except Exception as e:
        print("[shoemarker] Error:", e)
        raise e
    finally:
        driver.quit()


def click_3_likes(driver, main_url):
    try:
        driver.get(main_url)
        driver.implicitly_wait(5)
        # driver.execute_script("close_slidePopup();")
        like_button_1 = driver.find_element(By.XPATH, '//*[@id="BestNArrivalsProductList"]/ul/li[1]/div/button')
        driver.execute_script("arguments[0].click();", like_button_1)
        time.sleep(1)

        like_button_2 = driver.find_element(By.XPATH, '//*[@id="BestNArrivalsProductList"]/ul/li[2]/div/button')
        driver.execute_script("arguments[0].click();", like_button_2)
        time.sleep(1)

        like_button_3 = driver.find_element(By.XPATH, '//*[@id="BestNArrivalsProductList"]/ul/li[3]/div/button')
        driver.execute_script("arguments[0].click();", like_button_3)
        time.sleep(1)
    except Exception as e:
        print("[shoemarker] Error clicking likes:", e)
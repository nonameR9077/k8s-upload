# slack
import requests
from constants import SLACK_WEBHOOK_URL
def send_slack_message(text):
    requests.post(SLACK_WEBHOOK_URL, json={"text": text})

# captcha
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def try_captcha_attendance(driver, attendance_url, CAPTCHA_TRY_COUNT=7):
    for i in range(CAPTCHA_TRY_COUNT):
        print("attempt " + str(i+1))

        # access to attendance page
        driver.get(attendance_url)
        driver.implicitly_wait(5)  # wait for page to load

        time.sleep(1)

        # click attendance button
        driver.find_element(By.XPATH, '//*[@id="attendWriteForm"]/div/div[1]/span/a/img').click()

        time.sleep(1)

        PATH = os.getcwd() + "\\captcha_.PNG"

        capture_captcha(driver, '//*[@id="attendWriteForm"]/div/div[2]/div[1]/fieldset/p[1]/img', PATH)

        text = captcha_to_text(PATH)
        
        # if the length of the text is not correct retry
        if len(text) != 6:
            continue
        
        # input the captcha text into the input field
        captcha_input = driver.find_element(By.CSS_SELECTOR, "#secure_text.inputTypeText")
        # captcha_input.click()
        captcha_input.send_keys(text, Keys.RETURN)

        time.sleep(1)

        # click captcha OK button
        # driver.find_element(By.XPATH, '//*[@id="attendWriteForm"]/div/div[2]/div[2]/a[1]/img').click()
        
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        
        if alert.text != "보안문자가 일치하도록 입력해야 합니다.":
            # If the captcha is correct, break the loop
            try:
                print("[sofrano]", alert.text)
                alert.accept()
            except Exception as e:
                print(f"Error from attendance: {e}")
                # sys.exit(1)

            break
        else:
            # else just retry the captcha
            alert.accept()

def capture_captcha(driver, xpath, save_path="./captcha_.PNG"):
    try:
        wait = WebDriverWait(driver, 10)
        captcha_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        
        # scroll to the captcha element
        driver.execute_script("arguments[0].scrollIntoView(true);", captcha_element)
        time.sleep(1)
        
        # save the captcha image
        captcha_element.screenshot(save_path)
        print(f"image saved at: {save_path}")
        return save_path
    except Exception as e:
        print(f"An Error occured while saving: {e}")
        # sys.exit(1)

def captcha_to_text(captcha_image_path):
    import cv2
    import pytesseract
    import numpy as np

    image = cv2.imread(captcha_image_path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([0, 0, 0])  # 어두운 색 (글자)
    upper_bound = np.array([180, 255, 100])  # 연한 색 (노이즈)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    blur = cv2.GaussianBlur(thresh, (3,3), 0)

    # the path should be modified depending on your environment
    # remove if you are running this on a server
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\museo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist="0123456789abcdefghijklmnopqrstuvwxyz"'
    text = pytesseract.image_to_string(blur, config=custom_config, lang='eng')

    return text.strip()
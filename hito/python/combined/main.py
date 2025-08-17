import os
import re
from constants import *
from utils import get_bucket_data, save_bucket_data
from utils import send_slack_message, format_items
from crawler import init_driver, get_with_retry
from utils import date_to_isoformat, is_isoformat
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/secrets/gcs/key.json" # CREDENTIAL_PATH

def hito_update_check():
    driver = init_driver()
    data = get_bucket_data(BUCKET_NAME, HITO_FILE_NAME)

    NEW_FOUND = False
    NEW_MODIFIED = False

    try:
        for type_, items in data.items():
            if not items:
                continue
            for name, old_date in items.items():
                new_items = {}
                page = 1

                while True:
                    url = f"{HITO_URL}/{type_}/{name}-all.html?page={page}"
                    get_with_retry(driver, url)
                    driver.implicitly_wait(3)

                    try:
                        driver.find_element(By.XPATH, HITO_DATE_XPATH)
                    except:
                        send_slack_message(f"❌ {url} has no items.")
                        break

                    latest_date = date_to_isoformat(driver.find_element(By.XPATH, HITO_DATE_XPATH))

                    if not old_date:
                        send_slack_message(f"⚠️ {type_}:{name} has no date. Setting to {latest_date.isoformat()}")
                        data[type_][name] = latest_date.isoformat()
                        NEW_MODIFIED = True
                        break

                    if not is_isoformat(old_date):
                        send_slack_message(f"⚠️ {type_}:{name} has invalid date format. Updating.")
                        data[type_][name] = latest_date.isoformat()
                        NEW_MODIFIED = True
                        break

                    if latest_date <= datetime.fromisoformat(old_date):
                        break

                    cnt = 1
                    saved_cnt = 0
                    brk = False

                    while True:
                        try:
                            d = date_to_isoformat(driver.find_element(By.XPATH, f'/html/body/div/div[5]/div[{cnt}]/div[2]/p'))
                            if d <= datetime.fromisoformat(old_date):
                                brk = True
                                break

                            t = driver.find_element(By.XPATH, f'/html/body/div/div[5]/div[{cnt}]/h1/a').text
                            u = driver.find_element(By.XPATH, f'/html/body/div/div[5]/div[{cnt}]/h1/a').get_attribute("href")
                            ty = driver.find_element(By.XPATH, f'/html/body/div/div[5]/div[{cnt}]/div[2]/table/tbody/tr[2]/td[2]/a').text
                            l = driver.find_element(By.XPATH, f'/html/body/div/div[5]/div[{cnt}]/div[2]/table/tbody/tr[3]/td[2]/a').text

                            new_items[saved_cnt + cnt] = {
                                KEY_TITLE: t,
                                KEY_URL: u,
                                KEY_TYPE: ty,
                                KEY_LANG: l,
                                KEY_DATE: d.isoformat()
                            }

                        except NoSuchElementException:
                            page += 1
                            get_with_retry(driver, f"{HITO_URL}/{type_}/{name}-all.html?page={page}")
                            driver.implicitly_wait(3)
                            saved_cnt += cnt
                            cnt = 1
                            continue

                        cnt += 1

                    if brk:
                        break

                if new_items:
                    send_slack_message(f"🆕 {type_}:{name} has {len(new_items)} new items!\n\n{format_items(new_items)}")
                    data[type_][name] = latest_date.isoformat()
                    NEW_FOUND = True
                    NEW_MODIFIED = True

        if NEW_MODIFIED:
            save_bucket_data(BUCKET_NAME, HITO_FILE_NAME, data)

        if not NEW_FOUND:
            send_slack_message("😔 hito: No new items found today.")

    finally:
        driver.quit()


def ehan_update_check():
    driver = init_driver()
    data = get_bucket_data(BUCKET_NAME, EHEN_FILE_NAME)

    NEW_FOUND = False
    NEW_MODIFIED = False

    try:
        for type_, items in data.items():
            if not items:
                continue
            for name, old_date in items.items():
                new_items = {}
                page = 1

                while True:
                    url = f"{EHEN_URL}/tag/{type_}:{name}"
                    get_with_retry(driver, url)
                    driver.implicitly_wait(3)

                    try:
                        re.search(r'\d+', driver.find_element(By.XPATH, EHEN_RES_XPATH).text).group()
                    except:
                        send_slack_message(f"❌ {url} has no items. Is the URL correct?")
                        break

                    latest_date = date_to_isoformat(driver.find_element(By.XPATH, EHEN_DATE_XPATH).text)

                    if not old_date:
                        send_slack_message(f"⚠️ {type_}:{name} has no date. Setting to {latest_date.isoformat()}")
                        data[type_][name] = latest_date.isoformat()
                        NEW_MODIFIED = True
                        break

                    if not is_isoformat(old_date):
                        send_slack_message(f"⚠️ {type_}:{name} has invalid date format. Updating...")
                        data[type_][name] = latest_date.isoformat()
                        NEW_MODIFIED = True
                        break

                    if latest_date <= datetime.fromisoformat(old_date):
                        break

                    cnt = 1
                    saved_cnt = 0
                    brk = False

                    while True:
                        try:
                            d = date_to_isoformat(driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/table/tbody/tr[{cnt+1}]/td[2]/div[3]/div[1]').text)
                            if d <= datetime.fromisoformat(old_date):
                                brk = True
                                break

                            t = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/table/tbody/tr[{cnt+1}]/td[3]/a/div[1]').text
                            u = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/table/tbody/tr[{cnt+1}]/td[3]/a').get_attribute("href")
                            # l = driver.find_element(By.XPATH, f'/html/body/div/div[5]/div[{cnt}]/div[2]/table/tbody/tr[3]/td[2]/a').text

                            new_items[saved_cnt + cnt] = {
                                KEY_TITLE: t,
                                KEY_URL: u,
                                # KEY_TYPE: ty,
                                # KEY_LANG: l,
                                KEY_DATE: d.isoformat()
                            }

                        except NoSuchElementException:
                            page += 1
                            next_page_url = driver.find_element(By.XPATH, '//*[@id="unext"]').get_attribute("href")
                            if next_page_url is None:
                                brk = True
                                break

                            get_with_retry(driver, next_page_url)
                            driver.implicitly_wait(3)
                            saved_cnt += cnt
                            cnt = 1
                            continue

                        cnt += 1

                    if brk:
                        break

                if new_items:
                    send_slack_message(f"🆕 e-han: {type_}-{name} has {len(new_items)} new items!\n\n{format_items(new_items, False)}")
                    data[type_][name] = latest_date.isoformat()
                    NEW_FOUND = True
                    NEW_MODIFIED = True

        if NEW_MODIFIED:
            save_bucket_data(BUCKET_NAME, EHEN_FILE_NAME, data)

        if not NEW_FOUND:
            send_slack_message("😔 e-han: No new items found today.")

    finally:
        driver.quit()


def run_site_check(site_name, func):
    try:
        print(f"\n▶️  checking {site_name}...")
        func()
        print(f"\n✅ 완료!")
    except Exception as e:
        print(f"\n❌  Error occured while checking {site_name}: {e}")

if __name__ == "__main__":
    run_site_check("Hito", hito_update_check)
    # run_site_check("e-han", ehan_update_check)

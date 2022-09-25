import logging
import os
from datetime import date


from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def init():
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    opt = webdriver.ChromeOptions()
    opt.binary_location = os.getenv("GOOGLE_CHROME_SHIM")
    opt.add_argument("headless")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=opt)
    driver_wait = WebDriverWait(driver, 10)  # Timeout value (explicit wait)
    return driver, driver_wait


def login(driver: webdriver.Chrome):
    logging.debug("Attempt to login to SSO")
    driver.get("https://reseau-cd.360learning.com/")
    driver.find_element(By.ID, "ssoButton").click()
    driver.find_element(By.ID, "username").send_keys(os.getenv("USER"))
    driver.find_element(By.ID, "password").send_keys(os.getenv("PASS"))
    driver.find_element(By.NAME, "submit").click()
    return True


def get_timetable_page(
    driver: webdriver.Chrome, driver_wait: WebDriverWait, date_value: str
):
    logging.debug("Switch to the timetable page")
    driver_wait.until(
        ec.visibility_of_element_located((By.CLASS_NAME, "custom-link-container"))
    ).click()
    driver.switch_to.window(driver.window_handles[1])
    if date_value != None:
        format_date = date_value.split("/")
        format_date.reverse()
        final_date = "/".join(format_date)
        driver.get(
            driver.current_url.replace(date.today().strftime("%m/%d"), f"{final_date}")
        )
    return True


def get_date_week(driver: webdriver.Chrome):
    logging.debug("Retrieves the start and end date of the week")
    week_date = driver.find_elements(By.ID, "Jour")
    day_start_week = week_date[0].text
    day_end_week = week_date[4].text
    return day_start_week, day_end_week


def get_screenshot(driver: webdriver.Chrome):
    logging.debug("Taking the screenshot")
    driver.get_screenshot_as_file("timetable.png")
    return True

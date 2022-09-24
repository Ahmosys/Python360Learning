import logging
import os

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
    s = Service("chromedriver.exe")
    opt = webdriver.ChromeOptions()
    opt.add_argument("headless")
    opt.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=s, options=opt)
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


def get_timetable_page(driver: webdriver.Chrome, driver_wait: WebDriverWait):
    logging.debug("Switch to the timetable page")
    driver_wait.until(
        ec.visibility_of_element_located((By.CLASS_NAME, "custom-link-container"))
    ).click()
    driver.switch_to.window(driver.window_handles[1])
    return True


def get_screenshot(driver: webdriver.Chrome):
    logging.debug("Taking the screenshot")
    driver.get(driver.current_url.replace("09/24/2022", "10/22/2022"))
    driver.get_screenshot_as_file("edt.png")
    return True

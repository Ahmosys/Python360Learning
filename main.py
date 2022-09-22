import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# Vars
load_dotenv()
s = Service("chromedriver.exe")
opt = webdriver.ChromeOptions()
# opt.add_argument("headless")
opt.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=s, options=opt)
driver_wait = WebDriverWait(driver, 10)


# Login
driver.get("https://reseau-cd.360learning.com/")
driver.find_element(By.ID, "ssoButton").click()
driver.find_element(By.ID, "username").send_keys(os.getenv("USER"))
driver.find_element(By.ID, "password").send_keys(os.getenv("PASS"))
driver.find_element(By.NAME, "submit").click()
# Retrieve timetable
menu =  driver_wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/button")))
print(menu)



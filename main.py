from modules import scrapper


if __name__ == "__main__":
    driver, driver_wait = scrapper.init()
    scrapper.login(driver=driver)
    scrapper.get_timetable_page(driver=driver, driver_wait=driver_wait)
    scrapper.get_screenshot(driver=driver)
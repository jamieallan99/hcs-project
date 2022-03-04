from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def take_screenshot(url: str, class_name: str) -> None:
    options = Options()
    options.headless = True
    options.add_argument("--incognito")
    
    driver = webdriver.Chrome("./chromedriver.exe")

    driver.get(url)
    domain = url.split('.')[1]
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
    finally:
        pass

    try:
        driver.save_screenshot(f"{domain}_page.png")
        element.screenshot(f"{domain}_banner.png")
    finally:
        driver.quit()


take_screenshot('https://www.bbc.co.uk/news', 'bbccookies-banner')

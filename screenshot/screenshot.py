from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import platform

class SeleniumScreenshotter:

    def __init__(self, headless=False):
        options = Options()
        options.headless = headless  # Can be turned on if just taking the screenshots
        options.add_argument("--incognito")  # To ensure cookies aren't saved
        if platform.system() == 'Linux':
            self.driver = webdriver.Chrome("./screenshot/chromedriver", options=options)
        else: 
            self.driver = webdriver.Chrome("./screenshot/chromedriver.exe", options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 1024)

    def take_screenshot(self, url: str) -> None:
        self.driver.get(url)
        domain = url.split(':')[1].strip('/').replace('.', '_')

        # Trys to find an element containing "cookie" hopefully this will be a banner
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(., 'cookie')]"))
            )
        except Exception:
            print(f"Couldn't find banner for {url}")

        try:
            self.driver.save_screenshot(f"images/{domain}_page.png")
            #element.screenshot(f"{domain}_banner.png")
        except Exception:
            print(f"Couldn't save for {url}")
        return domain

    def quit(self):
        self.driver.quit()


# This will executed if the script is ran rather than imported
if __name__ == '__main__':
    urls = []  # Add some urls here 

    s = SeleniumScreenshotter()

    for url in urls:
        s.take_screenshot(url)

    s.quit()

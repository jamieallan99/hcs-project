from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SeleniumScreenshotter:

    def __init__(self):
        options = Options()
        # options.headless = True
        options.add_argument("--incognito")
        self.driver = webdriver.Chrome("./chromedriver.exe", options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 1024)

    def take_screenshot(self, url: str) -> None:
        self.driver.get(url)
        domain = url.strip('htps:/w.').split('.')[0]

        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(., 'cookie')]"))
            )
        except Exception:
            print(f"Couldn't find banner for {url}")
            return

        try:
            self.driver.save_screenshot(f"images/{domain}_page.png")
            #element.screenshot(f"{domain}_banner.png")
        except Exception:
            print(f"Couldn't save for {url}")
    
    def quit(self):
        self.driver.quit()


urls = ['https://google.com', 'https://blogger.com', 'https://facebook.com']

s = SeleniumScreenshotter()

for url in urls:
    s.take_screenshot(url)

s.quit()

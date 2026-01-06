from selenium.webdriver.chrome.webdriver import WebDriver

class Chrome(WebDriver):
    @property
    def is_closed(self) -> bool: ...

from typing import TypedDict

from selenium.webdriver.chrome.webdriver import WebDriver

class Cookie(TypedDict):
    domain: str
    expiry: int
    httpOnly: bool
    name: str
    path: str
    sameSite: str
    secure: int
    value: str

class Chrome(WebDriver):
    @property
    def is_closed(self) -> bool: ...
    def get_cookies(self) -> list[Cookie]: ...

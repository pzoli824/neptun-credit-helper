import abc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

class UnknownBrowserTypeException(Exception):
    "Raised when the browser type is not supported/unknown"
    pass
    
class BrowserType:
    CHROME = "chrome"

class Browser(abc.ABC):

    @property
    @abc.abstractmethod
    def driver(self) -> webdriver:
        pass


class ChromeBrowser(Browser):

    def __init__(self, mode: str = "production") -> None:
        if mode == "production":
            chromedriver_autoinstaller.install()
            self._driver = webdriver.Chrome(self._get_chrome_options())

    def _get_chrome_options(self) -> Options:
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument("--headless=new")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--incognito")
        return options

    @property
    def driver(self) -> webdriver:
        return self._driver
    
class BrowserFactory:
    mode = "production"

    @staticmethod
    def create_browser(type: BrowserType) -> Browser:
        match type:
            case BrowserType.CHROME:
                return ChromeBrowser(BrowserFactory.mode)
            case _:
                raise UnknownBrowserTypeException

import pytest

from pkg.providers.browser import BrowserFactory, BrowserType, ChromeBrowser, UnknownBrowserTypeException


class TestChromeBrowser:
    
    def test_chrome_browser_driver(self):
        chrome = ChromeBrowser()
        
        assert chrome.driver is not None    

class TestBrowserFactory:

    def test_browser_factory_create_browser_chrome(self):
        browser = BrowserFactory.create_browser(BrowserType.CHROME)
        
        assert browser is not None

    def test_browser_factory_create_browser_throw_unknown_browser_type_exception(self):
        with pytest.raises(UnknownBrowserTypeException) as excinfo:
            BrowserFactory.create_browser("something")


import pytest

from pkg.providers.browser import BrowserFactory, BrowserType, UnknownBrowserTypeException

class TestBrowserFactory:

    def test_browser_factory_create_browser_chrome(self):
        BrowserFactory.mode = "test"
        browser = BrowserFactory.create_browser(BrowserType.CHROME)
        
        assert browser is not None

    def test_browser_factory_create_browser_throw_unknown_browser_type_exception(self):
        with pytest.raises(UnknownBrowserTypeException) as excinfo:
            BrowserFactory.create_browser("something")


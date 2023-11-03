from pkg.providers.browser import BrowserFactory, BrowserType
from pkg.providers.neptun import Neptun, University

browser = BrowserFactory.create_browser(BrowserType.CHROME)
driver = browser.driver

neptun = Neptun(browser, University.SZTE)
neptun.login("username", "password")
neptun.get_all_course_informations()
import logging
import traceback
from pkg.providers.browser import BrowserFactory, BrowserType
from pkg.providers.neptun import Neptun, University

browser = BrowserFactory.create_browser(BrowserType.CHROME)
driver = browser.driver

neptun = Neptun(browser, University.SZTE)
neptun.login("username", "password")
try:
    neptun.get_all_course_informations()
    neptun.get_enrolled_courses_in_current_semester()

except Exception as e:
    logging.error(traceback.format_exc())

finally:
    neptun.logout_and_quit()
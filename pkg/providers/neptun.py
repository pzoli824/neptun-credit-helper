from pkg.providers.browser import Browser
from selenium.webdriver.common.by import By

class University:
    SZTE = "szte"

class NeptunPage:
    LOGIN = "/hallgato/login.aspx"
    SAMPLE_CURRICULUM = "/hallgato/main.aspx?ismenuclick=true&ctrl=02101"

class NeptunPageElement:
    LOGIN_BUTTON_ID = "btnSubmit"
    LOGIN_INPUT_USERNAME_ID = "user"
    LOGIN_INPUT_PASSWORD_ID = "pwd"


class Neptun:

    def __init__(self, b: Browser, university: University) -> None:
        self._browser = b.driver
        self._university = university
        self._base_url = f"https://neptun.{university}.hu"

    def _navigate_to(self, page: NeptunPage) -> None:
        url = f"{self._base_url}{page}"
        self._browser.get(url)

    def login(self, username: str, password: str) -> None:
        self._navigate_to(NeptunPage.LOGIN)

        username_input = self._browser.find_element(By.ID, NeptunPageElement.LOGIN_INPUT_USERNAME_ID)
        username_input.clear()
        username_input.send_keys(username)

        password_input = self._browser.find_element(By.ID, NeptunPageElement.LOGIN_INPUT_PASSWORD_ID)
        password_input.clear()
        password_input.send_keys(password)

        login_button = self._browser.find_element(By.ID, NeptunPageElement.LOGIN_BUTTON_ID)
        login_button.click()

    def logout(self) -> None:
        pass
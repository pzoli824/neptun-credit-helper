import pytest
from unittest.mock import Mock

from pkg.providers.neptun import Neptun, NeptunPage, NeptunPageElement, University

class TestNeptun:

    szte_base_url = f"https://neptun.{University.SZTE}.hu"

    def test_neptun_initialization(self):
        mock = Mock()
        neptun = Neptun(mock, University.SZTE)

        assert neptun._base_url == self.szte_base_url
        assert neptun._university is University.SZTE
        assert neptun._browser is mock.driver

    def test_neptun_login(self):
        mock = Mock()
        login_button_mock = Mock()
        expected_url = f"{self.szte_base_url}{NeptunPage.LOGIN}"
        mock.driver.find_element.return_value = login_button_mock
        neptun = Neptun(mock, University.SZTE)

        neptun.login("username", "password")

        assert mock.driver.get.call_count is 1
        assert mock.driver.find_element.call_count is 3
        mock.driver.get.assert_called_with(expected_url)
        assert login_button_mock.click.call_count is 1

    def test_neptun_get_enrolled_courses_in_current_semester(self):
        neptun_mock = Mock()
        expected_url = f"{self.szte_base_url}{NeptunPage.COURSES}"
        neptun_mock.driver.page_source = '<!DOCTYPE html><html><head><title>"Page Title"</title></head><body><table><tr id="tr__321"><td>1</td></tr></table></body></html>'
        neptun = Neptun(neptun_mock, University.SZTE)

        courses = neptun.get_enrolled_courses_in_current_semester()

        neptun_mock.driver.get.assert_called_with(expected_url)
        assert len(courses) is 1

    @pytest.mark.skip(reason="Fix test later")
    def test_neptun_get_all_course_informations(self):
        pass
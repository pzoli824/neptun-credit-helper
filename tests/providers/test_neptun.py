import pytest
from unittest.mock import Mock
from pkg.models.course import Course

from pkg.providers.neptun import Neptun, NeptunPage, University

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
        neptun_mock.driver.page_source = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>"Page Title"</title>
        </head>
        <body>
        <table>
        <tr id="tr__321"><td>1</td></tr>
        </table>
        </body></html>"""
        neptun = Neptun(neptun_mock, University.SZTE)

        courses = neptun.get_enrolled_courses_in_current_semester()

        neptun_mock.driver.get.assert_called_with(expected_url)
        assert len(courses) is 1

    def test_neptun_get_all_course_informations_return_with_one_leaf_course(self):
        neptun_mock = Mock()
        expected_url = f"{self.szte_base_url}{NeptunPage.SAMPLE_CURRICULUM}"
        neptun_mock.driver.page_source = self._create_html_mock_for_get_all_course_informations()
        neptun = Neptun(neptun_mock, University.SZTE)
        expected_courses = [
            Course("code_2", "name_2", "credit_2", "recommended_semester_2", "sample_curriculum_2", "course_group_code_2", "course_group_name_2", "course_type_2", "result_2", "course_enrollment_times_2"),
        ]

        courses_in_tree = neptun.get_all_course_informations()
        courses = courses_in_tree.getLeafNodesData()

        neptun_mock.driver.get.assert_called_with(expected_url)
        assert len(courses) is 1
        for i in range(len(courses)):
            assert str(courses[i]) == str(expected_courses[i])

    def test_neptun_get_all_course_informations_return_with_two_leaf_course(self):
        neptun_mock = Mock()
        expected_url = f"{self.szte_base_url}{NeptunPage.SAMPLE_CURRICULUM}"
        neptun_mock.driver.page_source = self._create_html_mock_for_get_all_course_informations(2)
        neptun = Neptun(neptun_mock, University.SZTE)
        expected_courses = [
            Course("code_2", "name_2", "credit_2", "recommended_semester_2", "sample_curriculum_2", "course_group_code_2", "course_group_name_2", "course_type_2", "result_2", "course_enrollment_times_2"),
            Course("code_3", "name_3", "credit_3", "recommended_semester_3", "sample_curriculum_3", "course_group_code_3", "course_group_name_3", "course_type_3", "result_3", "course_enrollment_times_3")
        ]

        courses_in_tree = neptun.get_all_course_informations()
        courses = courses_in_tree.getLeafNodesData()

        neptun_mock.driver.get.assert_called_with(expected_url)
        assert len(courses) is 2        
        for i in range(len(courses)):
            assert str(courses[i]) == str(expected_courses[i])

    def _create_html_mock_for_get_all_course_informations(self, leaf_nodes_count: int = 1) -> str:
        second_leaf_course_string = ""
        if leaf_nodes_count == 2:
            second_leaf_course_string = """
                <tr id="tr2__test3">
                    <td></td>
                    <td>code_3</td>
                    <td>name_3</td>
                    <td>credit_3</td>
                    <td>recommended_semester_3</td>
                    <td>sample_curriculum_3</td>
                    <td>course_group_code_3</td>
                    <td>course_group_name_3</td>
                    <td>course_type_3</td>
                    <td><div class="tooltipDetails">Some tooltip: </div>result_3</td>
                    <td>course_enrollment_times_3</td>
                </tr>
            """

        return """
        <!DOCTYPE html>
        <html>
        <head>
        <title>"Page Title"</title>
        </head>
        <body>
        <table>
            <tr id="unknown1">
            <td id="function_table_body">
                <table>
                <tr id="subrow_anything_0">
                    <td>
                    <table id="sub_test0">
                        <tr id="tr__test1">
                            <td></td>
                            <td>code_1</td>
                            <td>name_1</td>
                            <td>credit_1</td>
                            <td>recommended_semester_1</td>
                            <td>sample_curriculum_1</td>
                            <td>course_group_code_1</td>
                            <td>course_group_name_1</td>
                            <td>course_type_1</td>
                            <td><div class="tooltipDetails">Some tooltip: </div>result_1</td>
                            <td>course_enrollment_times_1</td>
                        </tr>
                        <tr id="subrow_anything_1">
                            <td>
                                <table id="sub_test1">
                                    <tr id="tr2__test2">
                                        <td></td>
                                        <td>code_2</td>
                                        <td>name_2</td>
                                        <td>credit_2</td>
                                        <td>recommended_semester_2</td>
                                        <td>sample_curriculum_2</td>
                                        <td>course_group_code_2</td>
                                        <td>course_group_name_2</td>
                                        <td>course_type_2</td>
                                        <td><div class="tooltipDetails">Some tooltip: </div>result_2</td>
                                        <td>course_enrollment_times_2</td>
                                    </tr>
                                    {second_leaf_course}
                                </table>
                            </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>""".format(second_leaf_course=second_leaf_course_string)    
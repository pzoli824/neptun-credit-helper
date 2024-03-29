import pytest

from typing import NamedTuple
from pkg.models.course import Course

class CourseAndExcepted(NamedTuple):
    '''Only used for testing'''
    course: Course
    expected_has_been_enrolled_to_course: bool

class CustomColumnForTest:
    text: str
    def __init__(self, text:str) -> None:
        self._text = text
    
    @property
    def text(self) -> str:
        return self._text

@pytest.fixture
def setup_courses_data() -> list[Course]:
    data = [
        Course("1"),
        Course("2"),
        Course("3"),
        Course("4"),
        Course("2"),
        Course("1"),
        Course("5"),
        Course("4"),
    ]
    yield data

class TestCourse:

    def test_course_initialization_by_constructor(self):
        course = Course("1", "test", "3", "4", "IKGB", "IKGB-345", "test name", "colloquium", "success (4)", "1")
        
        course.row_id = "2"
        course.parent_row_id = "5"

        assert course.parent_row_id is "5"
        assert course.row_id is "2"
        assert course._code is "1"
        assert course._recommended_semester is "4"
        assert course._course_enrollment_times is "1"

    def test_course_initialization_by_columns_static_methoh(self):
        parent_row_id = '3'
        row_id = '2'
        columns: list[CustomColumnForTest] = [
            CustomColumnForTest("DISPOSABLE!"),
            CustomColumnForTest("code"), 
            CustomColumnForTest("name"),
            CustomColumnForTest("credit"),
            CustomColumnForTest("4"),
            CustomColumnForTest("KB"),
            CustomColumnForTest("45"),
            CustomColumnForTest("group_name"),
            CustomColumnForTest("colloquium"),
            CustomColumnForTest("success (4)"),
            CustomColumnForTest("1"),
        ]

        course = Course.create_course_from_columns(columns, parent_row_id, row_id)
        print(course)

        assert course.parent_row_id is parent_row_id
        assert course.row_id is row_id
        assert course._code is 'code'   
        assert course._name is 'name'   
        assert course._credit is 'credit'   
        assert course._recommended_semester is '4'   
        assert course._sample_curriculum is 'KB'   
        assert course._course_group_code is '45'   
        assert course._course_group_name is 'group_name'   
        assert course._course_type is 'colloquium'   
        assert course._result == '4'   
        assert course._course_enrollment_times is '1'   

    def test_course_initialization_by_columns_static_method_column_short_length(self):
        columns: list[CustomColumnForTest] = [
        CustomColumnForTest("DISPOSABLE!"),
        CustomColumnForTest("code"), 
        CustomColumnForTest("name"),
        ]
        
        course = Course.create_course_from_columns(columns, '', '')

        assert course.parent_row_id is ''
        assert course.row_id is ''
        assert course._code is 'code'   
        assert course._name is 'name'   
        assert course._credit is ''   
        assert course._recommended_semester is ''   
        assert course._sample_curriculum is ''   
        assert course._course_group_code is ''   
        assert course._course_group_name is ''   
        assert course._course_type is ''   
        assert course._result is ''   
        assert course._course_enrollment_times is ''                     

    def test_course_eq_hash_with_set_collection(self, setup_courses_data: list[Course]):
        courses = set(setup_courses_data)

        assert len(courses) is 5

    def test_course_has_been_enrolled_to_course(self):
        test_data = [
            CourseAndExcepted(
                course=Course("", "", "", "", "", "", "", "", "", "1"),
                expected_has_been_enrolled_to_course=True
            ),
            CourseAndExcepted(
                course=Course("", "", "", "", "", "", "", "", "", "0"),
                expected_has_been_enrolled_to_course=False
            ),
            CourseAndExcepted(
                course=Course("", "", "", "", "", "", "", "", "", "aaaaa"),
                expected_has_been_enrolled_to_course=False
            ),
            CourseAndExcepted(
                course=Course("", "", "", "", "", "", "", "", "", ""),
                expected_has_been_enrolled_to_course=False
            )
        ]

        for data in test_data:
            result = data.course.has_been_enrolled_to_course()
            assert result is data.expected_has_been_enrolled_to_course        

    def test_course_has_been_completed(self):
        c1 = Course(result="dummy text")        
        c2 = Course(result="fail (1)")        
        c3 = Course(result="okayish (2)")

        assert c1.has_been_completed() is False        
        assert c2.has_been_completed() is False        
        assert c3.has_been_completed() is True

    def test_course_is_optional_to_choose(self):
        c1 = Course(course_type="Szabadon választható")        
        c2 = Course(course_type="Smth")        
        c3 = Course(course_type="Optional")        

        assert c1.is_optional_to_choose() is True        
        assert c2.is_optional_to_choose() is False        
        assert c3.is_optional_to_choose() is True        
                        
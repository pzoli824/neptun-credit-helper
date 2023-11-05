import pytest

from pkg.models.course import Course, ColumnsCourseField

class TestColumn:
    text: str
    def __init__(self, text:str) -> None:
        self._text = text
    
    @property
    def text(self) -> str:
        return self._text

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

    def test_course_initialization_by_static_method(self):
        parent_row_id = '3'
        row_id = '2'
        columns: list[TestColumn] = [
            TestColumn("DISPOSABLE!"),
            TestColumn("code"), 
            TestColumn("name"),
            TestColumn("credit"),
            TestColumn("4"),
            TestColumn("KB"),
            TestColumn("45"),
            TestColumn("group_name"),
            TestColumn("colloquium"),
            TestColumn("success (4)"),
            TestColumn("1"),
        ]

        course = Course.create_course_from_columns(columns, parent_row_id, row_id)

        assert course.parent_row_id is parent_row_id
        assert course.row_id is row_id
        assert course._code is 'code'   

    def test_course_print_str_represetation(self):
        assert False           
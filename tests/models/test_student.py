import pytest

from typing import NamedTuple
from pkg.models.course import Course
from pkg.models.student import Student

class CourseAndExcepted(NamedTuple):
    '''Only used for testing'''
    course: Course
    expected_has_been_enrolled_to_course: bool

class TestStudent:

    def test_student_has_been_enrolled_to_course(self):
        student = Student("test name")
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
            result = student._has_been_enrolled_to_course(data.course)
            assert result is data.expected_has_been_enrolled_to_course
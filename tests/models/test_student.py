import pytest
from pkg.models.course import Course, EnrolledCourse
from pkg.models.student import Student
from pkg.models.tree import Node, Tree

@pytest.fixture
def setup_enrolled_courses() -> list[EnrolledCourse]:
    data: list[EnrolledCourse] = [
        EnrolledCourse("1", "c1", "2", "1"),
        EnrolledCourse("2", "c2", "3", "1")
    ]
    yield data

@pytest.fixture
def setup_courses() -> Tree[Course]:
    t = Tree(Course())
    n1 = Node(Course(code="1", credit="2", result="(3)", course_enrollment_times="1", course_type="Elective"))
    n2 = Node(Course(code="2", credit="3", result="(1)", course_enrollment_times="2", course_type="Elective"))
    n3 = Node(Course(code="3", credit="1", result="(5)", course_enrollment_times="1", course_type="Optional"))
    n4 = Node(Course(code="4", credit="2", result="(4)", course_enrollment_times="2", course_type="Elective"))
    t.appendChildNodes(n1, n2, n3, n4)

    yield t

class TestStudent:

    def test_student_calculate_finished_credits(self, setup_courses: Tree[Course]):
        s = Student("test stud")
        s.all_courses = setup_courses

        credits = s.calculate_finished_credits()

        assert credits is 4

    def test_student_calculate_current_semester_credits(self, setup_enrolled_courses: list[EnrolledCourse]):
        s = Student("test stud")
        s.current_courses = setup_enrolled_courses

        credits = s.calculate_current_semester_credits()

        assert credits is 5
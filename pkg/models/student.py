
from pkg.models.course import Course, EnrolledCourse
from pkg.models.tree import Tree


class Student:
    _all_courses: Tree[Course] = None
    _current_courses: list[EnrolledCourse] = []

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def all_courses(self) -> Tree[Course]:
        return self._all_courses        

    @all_courses.setter 
    def all_courses(self, all_courses: Tree[Course]): 
        self._all_courses = all_courses

    @property
    def current_courses(self) -> list[EnrolledCourse]:
        return self._current_courses
   
    @current_courses.setter 
    def current_courses(self, current_courses: list[EnrolledCourse]): 
        self._current_courses = current_courses

    def calculate_finished_credits(self) -> int:
        courses = self._all_courses.getLeafNodesData()
        finished_credits = 0
        for course in courses:
            finished_credits += int(course.credit)

        return finished_credits    

    def calculate_current_semester_credits(self) -> int:
        credits = 0
        for current_course in self._current_courses:
            credits += int(current_course.credit)

        return credits    
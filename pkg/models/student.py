
from pkg.models.course import Course, EnrolledCourse
from pkg.models.tree import Tree


class Student:
    _all_courses: Tree[Course] = None
    _current_courses: list[EnrolledCourse] = []
    _neptun_code: str = "unknown"

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> str:
        self._name = new_name

    @property
    def neptun_code(self) -> str:
        return self._neptun_code

    @neptun_code.setter
    def neptun_code(self, new_neptun_code: str) -> str:
        self._neptun_code = new_neptun_code        

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
        courses = set(self._all_courses.get_leaf_nodes_data())
        finished_credits = 0
        for course in courses:
            if course.credit != '' and course.result != '' and course.has_been_enrolled_to_course() and course.has_been_completed() and not course.is_optional_to_choose():
                finished_credits += int(course.credit)

        return finished_credits    

    def calculate_current_semester_credits(self) -> int:
        credits = 0
        for current_course in self._current_courses:
            if current_course.credit != '':
                credits += int(current_course.credit)

        return credits    
    
    def calculate_credits_that_has_been_acquired_in_this_semester(self) -> int:
        all_courses: list[Course] = set(self._all_courses.get_leaf_nodes_data())
        current_courses: list[Course] = set(self.current_courses)
        current_courses_which_are_completed = list[Course]()
        for all_course in all_courses:
            for current_course in current_courses:
                if all_course == current_course:
                    current_courses_which_are_completed.append(all_course)

        credits = 0
        for c in current_courses_which_are_completed:
            if c.has_been_completed() and not c.is_optional_to_choose() and c.has_been_enrolled_to_course():
                credits += int(c.credit)
            
        return credits
import random
from pkg.models.student import Student
from pkg.models.course import EnrolledCourse, Course
from pkg.models.tree import Tree, Node

def data_test_student() -> Student:
    s = Student("Test Person")
    s.current_courses = data_test_enrolled_courses()
    s.all_courses = data_test_all_course()
    return s

def data_test_all_course() -> Tree[Course]:
    p1 = Node[Course](Course('', 'Test Parent Courses 1'))
    p2 = Node[Course](Course('', 'Test Parent Courses 2'))
    p3 = Node[Course](Course('', 'Test Parent Courses 3'))

    p1.append_child_nodes(
        Node[Course](Course('1', 'Test Course with long name 1', '2', '1', result='Teljesítés féléve: ', course_enrollment_times='')),
        Node[Course](Course('2', 'Test Course with long name 2', '3', '1', result='', course_enrollment_times='')),
        Node[Course](Course('3', 'Test Course with long name 3', '2', '1', result='Teljesítés féléve: Poor (2)', course_enrollment_times='1')),
        Node[Course](Course('4', 'Test Course 4', '2', '2', result='', course_enrollment_times='')),
        Node[Course](Course('5', 'Test Course with longer name 5', '5', '2', result='Teljesítés féléve: Average (3)', course_enrollment_times='1')),
        Node[Course](Course('6', 'Test Course 6', '4', '2', result='Good (4)', course_enrollment_times='2')),
        Node[Course](Course('7', 'Test Course with very very very long name 7', '2', '3', result='Excellent (5)', course_enrollment_times='1')),
        Node[Course](Course('8', 'Test Course 8', '2', '3', result='Poor (2)', course_enrollment_times='1'))     
    )
    p2.append_child_nodes(
        Node[Course](Course('9', 'Test Course with longer name 9', '1', '3', result='Average (3)', course_enrollment_times='3')),
        Node[Course](Course('10', 'Test Course 10', '2', '3', result='', course_enrollment_times='')),
        Node[Course](Course('11', 'Test Course 11', '3', '4', result='', course_enrollment_times='')),
        Node[Course](Course('12', 'Test Course with long name 12', '2', '4', result='', course_enrollment_times='')),
        Node[Course](Course('13', 'Test Course 13', '1', '4', result='', course_enrollment_times='')),
        Node[Course](Course('14', 'Test Course 14', '4', '4', result='', course_enrollment_times='')),
        Node[Course](Course('15', 'Test Course 15', '5', '4', result='', course_enrollment_times=''))
    )

    p3.append_child_nodes(
        *data_test_create_node_courses(16,70)
    )

    t = Tree[Course](Course())
    t.append_child_nodes(p1, p2, p3)
    return t

def data_test_create_node_courses(l: int, h: int) -> list[Node[Course]]:
    nodes: list[Node[Course]] = []
    for n in range(l,h):
        credit = random.randint(1, 5)
        semester = random.randint(1, 6)
        node = Node[Course](Course(f'{n}', f'Test Course {n}', f'{credit}', f'{semester}', result='', course_enrollment_times=''))
        nodes.append(node)

    return nodes

def data_test_enrolled_courses() -> list[EnrolledCourse]:
    return [
        EnrolledCourse('11', 'Test Course 11', '3', '1'),
        EnrolledCourse('12', 'Test Course 12', '2', '1'),
        EnrolledCourse('13', 'Test Course 13', '1', '1'),
        EnrolledCourse('14', 'Test Course 14', '4', '1'),
        EnrolledCourse('15', 'Test Course 15', '5', '1')
    ]
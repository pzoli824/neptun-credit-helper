import time
from typing import NamedTuple
from rich.console import Console, Group
from rich.layout import Layout
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
import keyboard
import platform
import os
import logging
from pkg.localization.localization import Localization
from pkg.localization.texts import AFTER_DOWN_ARROW_TEXT, AFTER_ESC_TEXT, AFTER_LEFT_ARROW_TEXT, AFTER_RIGHT_ARROW_TEXT, AFTER_UP_ARROW_TEXT, CHOOSE_UNIVERSITY, CODE, COMMANDS, COURSE_INFORMATIONS, CREDIT, CREDITS, CREDITS_ACQUIRED_CURRENT_SEMESTER, CREDITS_BEFORE_CURRENT_SEMESTER, DOWN_ARROW, ENROLLMENT_TIMES, ESC, GIVE_PASSWORD, GIVE_USERNAME, LEFT_ARROW, NEPTUN_CODE, OPTIONAL_COURSES_ARE_NOT_CALCULATED, PERSONAL_INFORMATIONS, PRESS_KEY, RECOMMENDED_SEMESTER, REQUIRED_CREDITS, RESULT, RIGHT_ARROW, TEXT_COMMANDS, NAME, TYPE, UP_ARROW
from pkg.models.auth import LoginCredentials
from pkg.models.course import ALL_REQUIRED_CREDIT
from pkg.models.pagination import Pagination
from pkg.models.student import Student
from pkg.providers.neptun import University

WAIT_TIME_AFTER_KEY_PRESS = 0.2

class DataLayout(NamedTuple):
    layout: Layout
    table: Table

class UITerminal:

    def __init__(self, student: Student, loc: Localization):
        self._console = Console()
        self._student = student
        self._all_course_pagination = Pagination(student.all_courses.get_leaf_nodes_data())
        self._loc = loc

    @staticmethod
    def get_login_credentials(loc: Localization) -> LoginCredentials:
        university = Prompt.ask(loc[CHOOSE_UNIVERSITY], choices=[University.SZTE])
        username = Prompt.ask(loc[GIVE_USERNAME])
        password = Prompt.ask(loc[GIVE_PASSWORD], password=True)
        return LoginCredentials(username, password, university)

    def home(self):
        self._console.clear()

        data_layout, table = self._get_data_layout_and_table()

        table_header_size = 3
        table_footer_size = 1
        data_layout_title_size = 1

        display_row_number = (self._console.height / 2) - (table_header_size + table_footer_size + data_layout_title_size)
        quantity = 0
        
        courses = self._all_course_pagination
        for course in courses:
            table.add_row(course.code, course.name, course.credit, course.recommended_semester, course.course_enrollment_times, course.course_type, course.result)
            data_layout.update(table)
            quantity += 1
            if table.row_count >= display_row_number:
                courses.set_quantity(quantity)
                break

        self._console.print(self._get_home_layout(self._get_informations_layout(), data_layout))
        self._listen_user_input()
    
    def _listen_user_input(self):
        while True:
            try:
                if keyboard.is_pressed('esc'):
                    break
                if keyboard.is_pressed('right arrow'):
                    self._home_courses_next_page()
                    time.sleep(WAIT_TIME_AFTER_KEY_PRESS)
                if keyboard.is_pressed('left arrow'):
                    self._home_courses_previous_page()    
                    time.sleep(WAIT_TIME_AFTER_KEY_PRESS)
                if keyboard.is_pressed('down arrow'):
                    self._home_courses_first_page()    
                    time.sleep(WAIT_TIME_AFTER_KEY_PRESS)    
                if keyboard.is_pressed('up arrow'):
                    self._home_courses_last_page()    
                    time.sleep(WAIT_TIME_AFTER_KEY_PRESS)                     
            except Exception as e:
                logging.error(e)
                break
        
        self._clear_system_console()

    def _clear_system_console(self):
        operation_system = platform.system()
        match operation_system:
            case "Windows":
                os.system("cls")
            case "Linux":
                os.system("clear")
            case _:
                logging.warning("Failed to clear system console")

    def _get_commands(self):
        loc = self._loc[COMMANDS]
        return Panel(
            Group(
                Text.assemble(f"{loc[PRESS_KEY]} ", (loc[ESC], "bold red"), f" {loc[AFTER_ESC_TEXT]}"),
                Text.assemble(f"{loc[PRESS_KEY]} ", (loc[LEFT_ARROW], "bold yellow"), f" {loc[AFTER_LEFT_ARROW_TEXT]}"),
                Text.assemble(f"{loc[PRESS_KEY]} ", (loc[RIGHT_ARROW], "bold yellow"), f" {loc[AFTER_RIGHT_ARROW_TEXT]}"),
                Text.assemble(f"{loc[PRESS_KEY]} ", (loc[DOWN_ARROW], "bold magenta"), f" {loc[AFTER_DOWN_ARROW_TEXT]}"),
                Text.assemble(f"{loc[PRESS_KEY]} ", (loc[UP_ARROW], "bold magenta"), f" {loc[AFTER_UP_ARROW_TEXT]}")
            ),
        title=self._loc[TEXT_COMMANDS]
        )

    def _get_personal_informations(self):
        credits = self._student.calculate_finished_credits()
        acquired_credits_in_current_semester = self._student.calculate_credits_that_has_been_acquired_in_this_semester()
        current_semester_credits = self._student.calculate_current_semester_credits()
        return Panel(
            Group(
                Text.assemble(f"{self._loc[NAME]}: ", (self._student.name, "bold yellow")),
                Text.assemble(f"{self._loc[NEPTUN_CODE]}: ", (self._student.neptun_code, "bold yellow")),
                Text.assemble(f"{self._loc[CREDITS]}: ", (str(credits), "bold green"), "/", str(ALL_REQUIRED_CREDIT)),
                Text.assemble(f"{self._loc[REQUIRED_CREDITS]}: ", (str(ALL_REQUIRED_CREDIT-credits), "bold red")),
                Text.assemble(f"{self._loc[CREDITS_BEFORE_CURRENT_SEMESTER]}: ", (str(credits-acquired_credits_in_current_semester), "bold green")),
                Text.assemble(f"{self._loc[CREDITS_ACQUIRED_CURRENT_SEMESTER]}: ", (str(acquired_credits_in_current_semester), "bold yellow"), "/", str(current_semester_credits)),
                Text.assemble((f"{self._loc[OPTIONAL_COURSES_ARE_NOT_CALCULATED]}!", "bold red"))
            ),
        title=self._loc[PERSONAL_INFORMATIONS]
        )

    def _get_courses_table_with_header(self):
        table = Table(expand=True, title=self._loc[COURSE_INFORMATIONS])

        table.add_column(self._loc[CODE], justify="center", style="cyan", no_wrap=True, ratio=2)
        table.add_column(self._loc[NAME], justify="center", style="magenta", no_wrap=True, ratio=9)
        table.add_column(self._loc[CREDIT], justify="center", style="green", no_wrap=True, ratio=3)
        table.add_column(self._loc[RECOMMENDED_SEMESTER], justify="center", style="green", no_wrap=True, ratio=4)
        table.add_column(self._loc[ENROLLMENT_TIMES], justify="center", style="green", no_wrap=True, ratio=4)
        table.add_column(self._loc[TYPE], justify="center", style="green", no_wrap=True, ratio=3)
        table.add_column(self._loc[RESULT], justify="center", style="green", no_wrap=True, ratio=4)

        return table
    
    def _get_home_layout(self, informations_layout: Layout, data_layout: Layout) -> Layout:
        home_layout = Layout()
        home_layout.split_column(
            informations_layout,
            data_layout
        )
        return home_layout

    def _get_informations_layout(self) -> Layout:
        informations_layout = Layout(name="informations")

        commands_layout = Layout(self._get_commands(), name="commands")
        personal_info_layout = Layout(self._get_personal_informations(), name="personal_info")

        informations_layout.split_row(commands_layout, personal_info_layout)
        return informations_layout
    
    def _get_data_layout_and_table(self) -> DataLayout:
        table = self._get_courses_table_with_header()
        data_layout = Layout(table, name="data")
        return DataLayout(layout=data_layout, table=table)

    def _home_courses_next_page(self):
        data_layout, table = self._get_data_layout_and_table()

        next_courses = self._all_course_pagination.get_next_page_elements()

        if len(next_courses) == 0:
            return

        for course in next_courses:
            table.add_row(course.code, course.name, course.credit, course.recommended_semester, course.course_enrollment_times, course.course_type, course.result)
            data_layout.update(table)
        
        self._console.clear()
        print(self._get_home_layout(self._get_informations_layout(), data_layout))

    def _home_courses_previous_page(self):
        data_layout, table = self._get_data_layout_and_table()

        previous_courses = self._all_course_pagination.get_previous_page_elements()

        if len(previous_courses) == 0:
            return

        for course in previous_courses:
            table.add_row(course.code, course.name, course.credit, course.recommended_semester, course.course_enrollment_times, course.course_type, course.result)
            data_layout.update(table)
        
        self._console.clear()
        print(self._get_home_layout(self._get_informations_layout(), data_layout))

    def _home_courses_first_page(self):
        data_layout, table = self._get_data_layout_and_table()

        first_page_courses = self._all_course_pagination.get_first_page_elements()    

        if len(first_page_courses) == 0:
            return
        
        for course in first_page_courses:
            table.add_row(course.code, course.name, course.credit, course.recommended_semester, course.course_enrollment_times, course.course_type, course.result)
            data_layout.update(table)
        
        self._console.clear()
        print(self._get_home_layout(self._get_informations_layout(), data_layout))

    def _home_courses_last_page(self):
        data_layout, table = self._get_data_layout_and_table()

        last_page_courses = self._all_course_pagination.get_last_page_elements()    

        if len(last_page_courses) == 0:
            return
        
        for course in last_page_courses:
            table.add_row(course.code, course.name, course.credit, course.recommended_semester, course.course_enrollment_times, course.course_type, course.result)
            data_layout.update(table)
        
        self._console.clear()
        print(self._get_home_layout(self._get_informations_layout(), data_layout))        
import time
from typing import NamedTuple
from rich.console import Console, Group
from rich.layout import Layout
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.align import Align
import keyboard
import platform
import os
import logging
from pkg.models.auth import LoginCredentials
from pkg.models.course import REQUIRED_CREDIT
from pkg.models.pagination import Pagination
from pkg.models.student import Student
from pkg.providers.neptun import University

WAIT_TIME_AFTER_KEY_PRESS = 0.2

class DataLayout(NamedTuple):
    layout: Layout
    table: Table

class UITerminal:

    def __init__(self, student: Student):
        self._console = Console()
        self._student = student
        self._all_course_pagination = Pagination(student.all_courses.getLeafNodesData())

    @staticmethod
    def get_login_credentials() -> LoginCredentials:
        university = Prompt.ask("Válassz egyetemet", choices=[University.SZTE])
        username = Prompt.ask("Add meg a felhasználóneved")
        password = Prompt.ask("Add meg a jelszavad", password=True)
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

        self._console.clear()
        print(self._get_home_layout(self._get_informations_layout(), data_layout))

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
            except:
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
        return Panel(
            Group(
                Text.assemble("- Nyomd meg az ", ("ESC", "bold red"), " billentyűt a kilépéshez!")
            ),
        title="Parancsok"
        )

    def _get_personal_informations(self):
        name = self._student.name
        credits = self._student.calculate_finished_credits()
        current_semester_credits = self._student.calculate_current_semester_credits()
        return Panel(
            Group(
                Text.assemble("Név: ", (name, "bold yellow")),
                Text.assemble("Kreditek: ", (str(credits), "bold red"), "/", str(REQUIRED_CREDIT)),
                Text.assemble("Szükséges kreditek: ", (str(REQUIRED_CREDIT-credits), "bold red")),
                Text.assemble("Eddig a megszerzett kreditek: ", (str(credits), "bold green")),
                Text.assemble("Ebben a szemeszterben csinált kreditek: ", (str(current_semester_credits), "bold yellow")),
                Text.assemble("Kreditek jelenlegi szemeszterrel bezáróan: ", (str(credits+current_semester_credits), "bold yellow"))
            ),
        title="Személyes adatok"
        )

    def _get_courses_table_with_header(self):
        table = Table(expand=True, title="Kurzus adatok")

        table.add_column("Kód", justify="center", style="cyan", no_wrap=True)
        table.add_column("Név", justify="center", style="magenta")
        table.add_column("Kredit", justify="center", style="green")
        table.add_column("Ajánlott szemeszter", justify="center", style="green")
        table.add_column("Felvételek száma", justify="center", style="green")
        table.add_column("Típus", justify="center", style="green")
        table.add_column("Eredmény", justify="center", style="green")

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
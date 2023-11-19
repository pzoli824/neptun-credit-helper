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
from pkg.models.student import Student

from pkg.providers.neptun import University



class UITerminal:

    def __init__(self, student: Student):
        self._console = Console()
        self._student = student

    @staticmethod
    def get_login_credentials() -> LoginCredentials:
        university = Prompt.ask("Válassz egyetemet", choices=[University.SZTE])
        username = Prompt.ask("Add meg a felhasználóneved")
        password = Prompt.ask("Add meg a jelszavad", password=True)
        return LoginCredentials(username, password, university)

    def home(self):
        self._console.clear()
        main_layout = Layout()
        data_layout = Layout(self._get_courses_in_table(), name="data")

        main_layout.split_column(
            Layout(name="informations"),
            Align.center(data_layout, vertical="middle")
        )

        commands_layout = Layout(self._get_commands(), name="commands")
        personal_info_layout = Layout(self._get_personal_informations(), name="personal_info")

        main_layout["informations"].split_row(
            commands_layout,
            personal_info_layout,
        )

        print(main_layout)
        self._listen_user_input()

    def _listen_user_input(self):
        while True:
            try:
                if keyboard.is_pressed('esc'):
                    break
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

    def _get_courses_in_table(self):
        table = Table()

        table.add_column("Kód", justify="center", style="cyan", no_wrap=True)
        table.add_column("Név", justify="center", style="magenta")
        table.add_column("Kredit", justify="center", style="green")
        table.add_column("Ajánlott szemeszter", justify="center", style="green")
        table.add_column("Felvételek száma", justify="center", style="green")
        table.add_column("Típus", justify="center", style="green")
        table.add_column("Eredmény", justify="center", style="green")

        courses = self._student.all_courses.getLeafNodesData()
        for course in courses:
            table.add_row(course.code, course.name, course.credit, course.recommended_semester, course.course_enrollment_times, course.course_type, course.result)

        return Panel(
            table,
            title="Kurzus adatok"
        )
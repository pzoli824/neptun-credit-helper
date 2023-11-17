from rich.console import Console, Group
from rich.layout import Layout
from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table


from pkg.providers.neptun import University



class UITerminal:

    def __init__(self):
        self._console = Console()

    def login(self):
        university = Prompt.ask("Válassz egyetemet", choices=[University.SZTE])
        username = Prompt.ask("Add meg a felhasználóneved")
        password = Prompt.ask("Add meg a jelszavad", password=True)

    def home(self):
        main_layout = Layout()
        data_layout = Layout(self._get_courses_in_table(), name="data")

        main_layout.split_column(
            Layout(name="informations"),
            data_layout
        )

        commands_layout = Layout(self._get_commands(), name="commands")
        personal_info_layout = Layout(self._get_personal_informations(), name="personal_info")

        main_layout["informations"].split_row(
            commands_layout,
            personal_info_layout,
        )

        print(main_layout)    

    def _get_commands(self):
        return Panel(
            Group(
                Text.assemble("- press ", ("1", "bold yellow"), " to change subject view to detailed mode."),
                Text.assemble("- press ", ("ESC", "bold red"), " to exit program.")
            ),
        title="Parancsok"
        )

    def _get_personal_informations(self):
        return Panel(
            Group(
                Text.assemble("Név: ", ("Teszt személy", "bold yellow")),
                Text.assemble("Kreditek: ", ("150", "bold red"), "/180"),
                Text.assemble("Szükséges kreditek: ", ("30", "bold red")),
                Text.assemble("Ebben a félévben csinált kreditek: ", ("22", "bold yellow")),
                Text.assemble("Eddig a megszerzett kreditek: ", ("150", "bold green"))
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



        table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
        table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
        table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
        table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")
                              
        return Panel(
            table,
            title="Kurzus adatok"
        )
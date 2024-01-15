import logging
import os
import click
import sys
from data.student import data_test_student
from pkg.localization.localization import Language, Localization
from pkg.localization.texts import CHOOSE_LANGUAGE
from pkg.models.student import Student
from pkg.providers.browser import BrowserFactory, BrowserType
from pkg.providers.neptun import Neptun
from pkg.ui.terminal import UITerminal
from rich.prompt import Prompt

sys.setrecursionlimit(2000)

@click.group()
def cli():
    pass

@cli.command()
def run():
    '''Runs the application in production mode'''
    loc = create_localization()
    browser = BrowserFactory.create_browser(BrowserType.CHROME)
    credentials = UITerminal.get_login_credentials(loc)
    neptun = Neptun(browser, credentials.university)
    neptun.login(credentials.username, credentials.password)

    student = Student("test name")
    #TODO get student name too
    try:
        student.all_courses = neptun.get_all_course_informations()
        student.current_courses = neptun.get_enrolled_courses_in_current_semester()

    except Exception as e:
        logging.error(e)

    finally:
        neptun.logout_and_quit()
        ui = UITerminal(student, loc)
        ui.home()



@cli.command()
def test_run():
    '''Runs the application in test mode, with test data'''
    loc = create_localization()
    ui = UITerminal(data_test_student(), loc)
    ui.home()


def create_localization() -> Localization:
    path = os.path.dirname(os.path.abspath(__file__))
    localization_file_path = f"{path}/pkg/localization/localization.yaml"
    loc = Localization(localization_file_path, Language.ENGLISH)

    language = Prompt.ask(loc[CHOOSE_LANGUAGE], choices=[Language.HUNGARY, Language.ENGLISH])
    loc.language = language
    return loc


if __name__ == '__main__':
    cli()
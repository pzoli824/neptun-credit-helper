import logging
import click
import sys
from data.student import data_test_student
from pkg.models.student import Student
from pkg.providers.browser import BrowserFactory, BrowserType
from pkg.providers.neptun import Neptun
from pkg.ui.terminal import UITerminal

sys.setrecursionlimit(2000)

@click.group()
def cli():
    pass

@cli.command()
def run():
    '''Runs the application in production mode'''
    browser = BrowserFactory.create_browser(BrowserType.CHROME)

    credentials = UITerminal.get_login_credentials()
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
        ui = UITerminal(student)
        ui.home()



@cli.command()
def test_run():
    '''Runs the application in test mode, with test data'''
    ui = UITerminal(data_test_student())
    ui.home()


if __name__ == '__main__':
    cli()
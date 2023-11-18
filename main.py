import logging
import traceback
import click
from pkg.providers.browser import BrowserFactory, BrowserType
from pkg.providers.neptun import Neptun, University
from pkg.ui.terminal import UITerminal

@click.group()
def cli():
    pass

@cli.command()
def run():
    '''Runs the application in production mode'''
    browser = BrowserFactory.create_browser(BrowserType.CHROME)
    driver = browser.driver

    neptun = Neptun(browser, University.SZTE)
    neptun.login("username", "password")
    try:
        neptun.get_all_course_informations()
        neptun.get_enrolled_courses_in_current_semester()

    except Exception as e:
        logging.error(traceback.format_exc())

    finally:
        neptun.logout_and_quit()


@cli.command()
def test_run():
    '''Runs the application in test mode, with test data'''
    click.echo('test run')
    ui = UITerminal()


if __name__ == '__main__':
    cli()
import logging
import traceback

from bs4 import BeautifulSoup
from pkg.models.course import Course
from pkg.models.tree import Tree, Node
from pkg.providers.browser import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class University:
    SZTE = "szte"

class NeptunPage:
    LOGIN = "/hallgato/login.aspx"
    SAMPLE_CURRICULUM = "/hallgato/main.aspx?ismenuclick=true&ctrl=02101"

class NeptunPageElement:
    LOGIN_BUTTON_ID = "btnSubmit"
    LOGIN_INPUT_USERNAME_ID = "user"
    LOGIN_INPUT_PASSWORD_ID = "pwd"

    AFTER_LOGIN_MESSAGES_TABLE_HEADER_ID = "function_tableheader"
    LOGOUT_ELEMENT_ID = "lbtnQuit"

    FILTER_BY_ALL_COURSES_CHECK_BOX_ID = "upFilter_rbtnCompleted_0"
    QUERY_ALL_COURSES_INFORMATION_BUTTON_ID = "upFilter_expandedsearchbutton"
    SAMPLE_CURRICULUM_RETRIEVED_TABLE_ID = "head_Code"
    SAMPLE_CURRICULUM_COURSE_TABLE_TOP_ROWS_XPATH = "//*[contains(@id, 'tr__')]"
    SAMPLE_CURRICULUM_COURSE_TABLE_ROW_COLUMNS_XPATH = ".//td"

    @staticmethod
    def get_sample_curriculum_course_table_top_rows_by_level_xpath(id: str, level: int) -> str:
        if level < 2:
            return f"//*[contains(@id, 'tr__')]"
        else:
            return f"//tr[@id='trs__{id}']//descendant::tr[contains(@id, 'tr{level}__')]"
        
TABLE_NO_ROW_FOUND = 0

class Neptun:

    def __init__(self, b: Browser, university: University) -> None:
        self._browser = b.driver
        self._university = university
        self._base_url = f"https://neptun.{university}.hu"

    def _navigate_to(self, page: NeptunPage) -> None:
        url = f"{self._base_url}{page}"
        self._browser.get(url)

    def login(self, username: str, password: str) -> None:
        self._navigate_to(NeptunPage.LOGIN)

        username_input = self._browser.find_element(By.ID, NeptunPageElement.LOGIN_INPUT_USERNAME_ID)
        username_input.clear()
        username_input.send_keys(username)

        password_input = self._browser.find_element(By.ID, NeptunPageElement.LOGIN_INPUT_PASSWORD_ID)
        password_input.clear()
        password_input.send_keys(password)

        login_button = self._browser.find_element(By.ID, NeptunPageElement.LOGIN_BUTTON_ID)
        login_button.click()

    def get_all_course_informations(self) -> Tree[Course]:
        try:
            WebDriverWait(self._browser, 15).until(
                EC.presence_of_element_located((By.ID, NeptunPageElement.AFTER_LOGIN_MESSAGES_TABLE_HEADER_ID))
            )
            self._navigate_to(NeptunPage.SAMPLE_CURRICULUM)
            self._browser.find_element(By.ID, NeptunPageElement.FILTER_BY_ALL_COURSES_CHECK_BOX_ID).click()
            self._browser.find_element(By.ID, NeptunPageElement.QUERY_ALL_COURSES_INFORMATION_BUTTON_ID).click()

            try:
                # wait for results
                WebDriverWait(self._browser, 15).until(
                    EC.presence_of_element_located((By.ID, NeptunPageElement.SAMPLE_CURRICULUM_RETRIEVED_TABLE_ID))
                )

                html = self._browser.page_source
                soup = BeautifulSoup(html, "html5lib")
                table_body = soup.find('td', id='function_table_body')
                soup = BeautifulSoup(str(table_body), "html5lib")
                lowest_level = self._get_table_lowest_row_level(soup, 1)
                tree = self._get_table_rows_in_array_from_lowest_level_to_highest(soup, lowest_level)

            except Exception as e:
                logging.error(traceback.format_exc())

            finally:
                self._logout_and_quit()
                print("logged out and quited")

        except TimeoutException:
            self._browser.quit()

        finally:
            return []
        
    def _get_table_rows_in_array_from_lowest_level_to_highest(self, soup: BeautifulSoup, lowest_level: int) -> Tree[Course]:
        previous_course_nodes = list[Node[Course]]()
        for level in range(lowest_level,1,-1):
            row_level_id = "tr__"
            if level > 1: 
                row_level_id = f"tr{level}__"
            
            rows = soup.find_all('tr', id=lambda e: e and e.startswith(row_level_id))
            current_course_nodes = list[Node[Course]]()
            for row in rows:
                unsplitted_row_id = row.find_parent('table')['id'].split('__')
                parent_row_id = ''
                if len(unsplitted_row_id) > 1:
                    parent_row_id = unsplitted_row_id[1]
                row_id = row.get('id')
                columns = row.select('td')
                course = Course.create_course_from_columns(columns, parent_row_id, row_id)
                current_course_node = Node[Course](course)
                if len(previous_course_nodes) == 0:
                    previous_course_nodes.append(current_course_node)
                    continue
                else:
                    for previous_course_node in previous_course_nodes:
                        if course.row_id == previous_course_node.data.parent_row_id:
                            current_course_node.appendChildNodes(previous_course_node)
                    
                    current_course_nodes.append(current_course_node)

            previous_course_nodes = current_course_nodes

        tree = Tree[Course](Course("", "", "", "", "", "", "", "", "", ""))
        tree.appendChildNodes(*previous_course_nodes)
        return tree

    def _get_table_lowest_row_level(self, soup: BeautifulSoup, level: int) -> int:
            row_level_id = "tr__"
            if level > 1: 
                row_level_id = f"tr{level}__"

            rows = soup.find_all('tr', id=lambda e: e and e.startswith(row_level_id))
            if len(rows) == 0 and level == 1:
                return TABLE_NO_ROW_FOUND
            elif len(rows) == 0 and level > 1:
                return level-1

            return self._get_table_lowest_row_level(soup, level+1)

    def _logout_and_quit(self) -> None:
        self._browser.find_element(By.ID, NeptunPageElement.LOGOUT_ELEMENT_ID).click()
        self._browser.quit()
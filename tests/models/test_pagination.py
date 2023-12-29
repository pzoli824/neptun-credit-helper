
import pytest

from pkg.models.pagination import Pagination

@pytest.fixture
def setup_data():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    yield data

class TestPagination:

    def test_pagination_get_current_page_elements(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        data = number_pages.get_current_page_elements()
        expected_result = [1, 2, 3 , 4, 5]

        for i in range(len(data)):
            assert data[i] is expected_result[i]

    def test_pagination_get_next_page_elements_higher_page_index_than_max_length(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 12
        data = number_pages.get_next_page_elements()
        expected_result = [11, 12, 13]

        for i in range(len(data)):
            assert data[i] is expected_result[i]

    def test_pagination_get_next_page_elements_lesser_page_index_than_max_length(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 8
        data = number_pages.get_next_page_elements()
        expected_result = [6, 7, 8, 9, 10]

        for i in range(len(data)):
            assert data[i] is expected_result[i]            

    def test_pagination_get_previous_page_elements_higher_than_quantity(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 6
        data = number_pages.get_previous_page_elements()
        expected_result = [6, 7, 8, 9, 10]

        for i in range(len(data)):
            assert data[i] is expected_result[i]            

    def test_pagination_get_previous_page_elements_lesser_than_quantity(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 3
        data = number_pages.get_previous_page_elements()
        expected_result = [1, 2, 3, 4, 5]

        for i in range(len(data)):
            assert data[i] is expected_result[i]             
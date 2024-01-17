
import pytest

from pkg.models.pagination import Pagination

@pytest.fixture
def setup_data():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    yield data

class TestPagination:

    def test_pagination_get_current_page_elements(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        expected_result = [1, 2, 3 , 4, 5]

        data = number_pages.get_current_page_elements()

        for i in range(len(data)):
            assert data[i] is expected_result[i]

    def test_pagination_get_next_page_elements_higher_page_index_than_max_length(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 12

        data = number_pages.get_next_page_elements()

        assert len(data) is 0

    def test_pagination_get_next_page_elements_lesser_page_index_than_max_length_case_1(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 8
        expected_result = [11, 12, 13]

        data = number_pages.get_next_page_elements()

        if len(data) == 0:
            raise AssertionError
        for i in range(len(data)):
            assert data[i] is expected_result[i]            

    def test_pagination_get_next_page_elements_lesser_page_index_than_max_length_case_2(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 2
        expected_result = [6, 7, 8, 9, 10]

        data = number_pages.get_next_page_elements()

        if len(data) == 0:
            raise AssertionError
        for i in range(len(data)):
            assert data[i] is expected_result[i] 

    def test_pagination_get_previous_page_elements_higher_than_quantity(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 9
        expected_result = [1, 2, 3, 4, 5]

        data = number_pages.get_previous_page_elements()

        if len(data) == 0:
            raise AssertionError
        for i in range(len(data)):
            assert data[i] is expected_result[i]            

    def test_pagination_get_previous_page_elements_equal_or_lesser_than_quantity(self, setup_data):
        number_pages = Pagination(setup_data, 5)
        number_pages._page_index = 4
        expected_result = [1, 2, 3, 4, 5]

        data = number_pages.get_previous_page_elements()

        if len(data) == 0:
            raise AssertionError
        for i in range(len(data)):
            assert data[i] is expected_result[i]             

    def test_pagination_iterator(self, setup_data: list[int]):
        number_pages = Pagination(setup_data, 5)
        expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        for i in range(len(number_pages)):
            assert number_pages[i] is expected_result[i]

        incr = 0
        for item in number_pages:
            assert item is expected_result[incr]
            incr += 1

    def test_pagination_get_page_number(self, setup_data: list[int]):
        number_pages = Pagination(setup_data, 5)

        number_pages.get_next_page_elements()
        number_pages.get_next_page_elements()
        page = number_pages.get_page_number()

        assert page is 3
    
    def test_pagination_get_last_page_number(self, setup_data: list[int]):
        number_pages = Pagination(setup_data, 15)

        page = number_pages.get_last_page_number()

        assert page is 1    

    def test_pagination_methods_with_empty_input_and_zero_quantity(self):
        number_pages = Pagination([], 0)

        current_page = number_pages.get_page_number()
        page = number_pages.get_last_page_number()
        first_page_elements = number_pages.get_first_page_elements()
        current_page_elements = number_pages.get_current_page_elements()
        last_page_elements = number_pages.get_last_page_elements()
        previous_page_elements = number_pages.get_previous_page_elements()
        next_page_elements = number_pages.get_next_page_elements()

        assert current_page is 1
        assert page is 1         
        assert len(first_page_elements) is 0         
        assert len(current_page_elements) is 0         
        assert len(last_page_elements) is 0         
        assert len(previous_page_elements) is 0         
        assert len(next_page_elements) is 0         
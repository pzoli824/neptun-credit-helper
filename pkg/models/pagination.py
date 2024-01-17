
import math
from typing import Generic, TypeVar

T = TypeVar("T")

class Pagination(Generic[T]):

    def __init__(self, data: list[T], quantity = 5) -> None:
        self._data = data
        self._page_index = 0
        self._quantity = quantity

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i < len(self._data):
            data = self._data[self._i]
            self._i += 1
            return data
        else:
            raise StopIteration

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index): 
        return self._data[index]       

    def _get_page_start_index(self) -> int:
        page = self._page_index / self._quantity
        return math.floor(page) * self._quantity

    def set_quantity(self, quantity):
        self._quantity = quantity

    def get_page_number(self) -> int:
        page = self._page_index / self._quantity
        if page <= 1:
            page = 1
        else:
            page = math.floor(page)
            
        return page

    def get_first_page_elements(self) -> list[T]:
        if self._page_index == 0:
            return []
        self._page_index = 0
        return self._data[self._page_index:self._quantity:1]
    
    def get_last_page_elements(self) -> list[T]:
        page_in_float = len(self._data) / self._quantity
        first_index_of_last_page = math.floor(page_in_float) * self._quantity
        if self._page_index == first_index_of_last_page:
            return []
        
        self._page_index = first_index_of_last_page
        remaining_quantity = first_index_of_last_page + (len(self._data) - first_index_of_last_page)
        return self._data[self._page_index:remaining_quantity:1]

    def get_current_page_elements(self) -> list[T]:
        index = self._page_index
        data = []

        if index + self._quantity <= len(self._data):
            data = self._data[index:self._quantity:1]
        else:
            remaining_quantity = (index + self._quantity) - len(self._data)
            data = self._data[index:remaining_quantity:1]

        return data

    def get_next_page_elements(self) -> list[T]:
        if self._page_index >= len(self._data):
            return []
        
        index = self._page_index + self._quantity
        data = []

        if index <= len(self._data):
            self._page_index = index
            page_start_index = self._get_page_start_index()
            data = self._data[page_start_index:page_start_index+self._quantity:1]
        else:
            remaining_quantity = index - (index - len(self._data))
            self._page_index = self._page_index + remaining_quantity
            page_start_index = self._get_page_start_index()
            data = self._data[page_start_index:page_start_index+remaining_quantity:1]

        if self._page_index > len(self._data):
            self._page_index = len(self._data)

        return data

    def get_previous_page_elements(self) -> list[T]:
        if self._page_index <= 0:
            return []
        
        index = self._page_index + 1
        page_original_array_index = self._page_index
        data = []

        if index >= self._quantity:
            self._page_index = page_original_array_index - self._quantity
            if self._page_index < 0:
                self._page_index = 0
            page_start_index = self._get_page_start_index()
            data = self._data[page_start_index:page_start_index+self._quantity:1]
        else:
            self._page_index = 0
            remaining_quantity = index
            data = self._data[self._page_index:self._page_index+remaining_quantity:1]

        if self._page_index < 0:
            self._page_index = 0

        return data
    
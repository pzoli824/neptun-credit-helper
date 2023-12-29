
import math
from typing import Generic, TypeVar

T = TypeVar("T")

class Pagination(Generic[T]):

    def __init__(self, data: list[T], quantity = 5) -> None:
        self._data = data
        self._page_index = 0
        self._quantity = quantity

    def set_quantity(self, quantity):
        self._quantity = quantity

    def get_page_number(self) -> int:
        page = self._page_index / self._quantity
        if page < 1:
            page = 1
        else:
            page = math.floor(page)
            
        return page

    def get_first_page(self) -> list[T]:
        self._page_index = 0
        return self._data[self._page_index, self._quantity, 1]

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
        if self._page_index == len(self._data):
            return []
        
        index = self._page_index
        data = []

        if index + self._quantity <= len(self._data):
            data = self._data[index:self._quantity:1]
            self._page_index = index + self._quantity
        else:
            remaining_quantity = (index + self._quantity) - len(self._data)
            data = self._data[index:remaining_quantity:1]
            self._page_index = index + remaining_quantity

        return data

    def get_previous_page_elements(self) -> list[T]:
        if self._page_index == 0:
            return []
        
        index = self._page_index
        data = []

        if index >= self._quantity:
            data = self._data[index - self._quantity:self._quantity:1]
            self._page_index = index - self._quantity
        else:
            remaining_quantity = index
            data = self._data[index:remaining_quantity:1]
            self._page_index = 0

        return data
    
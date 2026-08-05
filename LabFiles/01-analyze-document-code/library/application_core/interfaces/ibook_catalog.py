from abc import ABC, abstractmethod
from typing import Optional
from ..entities.book import Book
from ..entities.book_item import BookItem
from ..entities.loan import Loan


class IBookCatalog(ABC):
    @abstractmethod
    def search_books_by_title(self, title_input: str) -> list[Book]:
        pass

    @abstractmethod
    def get_book_availability(self, book_id: int) -> tuple[bool, Optional[Loan], Optional[BookItem]]:
        pass

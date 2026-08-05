from typing import Optional
from application_core.entities.book import Book
from application_core.entities.book_item import BookItem
from application_core.entities.loan import Loan
from application_core.interfaces.ibook_catalog import IBookCatalog
from .json_data import JsonData


class JsonBookCatalog(IBookCatalog):
    def __init__(self, json_data: JsonData):
        self._json_data = json_data

    def search_books_by_title(self, title_input: str) -> list[Book]:
        normalized = title_input.strip().casefold()

        exact_matches = [
            book for book in self._json_data.books
            if book.title.casefold() == normalized
        ]
        partial_matches = [
            book for book in self._json_data.books
            if normalized in book.title.casefold() and book not in exact_matches
        ]

        return exact_matches + partial_matches

    def get_book_availability(self, book_id: int) -> tuple[bool, Optional[Loan], Optional[BookItem]]:
        related_items = [
            book_item for book_item in self._json_data.book_items
            if book_item.book_id == book_id
        ]
        if not related_items:
            return False, None, None

        related_item_ids = {book_item.id for book_item in related_items}
        active_loans = [
            loan for loan in self._json_data.loans
            if loan.book_item_id in related_item_ids and loan.return_date is None
        ]

        active_item_ids = {loan.book_item_id for loan in active_loans}
        available_item = next(
            (book_item for book_item in related_items if book_item.id not in active_item_ids),
            None,
        )
        if available_item is not None:
            return True, None, available_item

        active_loans_sorted = sorted(
            active_loans,
            key=lambda loan: loan.due_date if loan.due_date is not None else float("inf"),
        )
        return False, active_loans_sorted[0] if active_loans_sorted else None, None

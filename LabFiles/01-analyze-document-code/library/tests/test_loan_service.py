import unittest
from unittest.mock import MagicMock
from application_core.services.loan_service import LoanService
from application_core.entities.loan import Loan
from application_core.entities.patron import Patron
from application_core.enums.loan_extension_status import LoanExtensionStatus
from application_core.enums.loan_return_status import LoanReturnStatus
from datetime import datetime, timedelta

class LoanServiceTest(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = LoanService(self.mock_repo)

    def test_extend_loan_success(self):
        print("Executando test_extend_loan_success...")
        patron = Patron(id=1, name="John Doe", membership_end=datetime.now()+timedelta(days=1), membership_start=datetime.now()-timedelta(days=30))
        loan = Loan(id=1, book_item_id=1, patron_id=1, patron=patron, loan_date=datetime.now()-timedelta(days=2), due_date=datetime.now()+timedelta(days=1))
        self.mock_repo.get_loan.return_value = loan
        status = self.service.extend_loan(1)
        print(f"status de extend_loan: {status}")
        self.assertEqual(status, LoanExtensionStatus.SUCCESS)

    def test_return_loan_not_found(self):
        print("Executando test_return_loan_not_found...")
        self.mock_repo.get_loan.return_value = None
        status = self.service.return_loan(1)
        print(f"status de return_loan: {status}")
        self.assertEqual(status, LoanReturnStatus.LOAN_NOT_FOUND)

    def test_checkout_loan_success(self):
        print("Executando test_checkout_loan_success...")
        self.mock_repo.get_loans.return_value = []

        def add_loan_side_effect(loan):
            return loan

        self.mock_repo.add_loan.side_effect = add_loan_side_effect
        new_loan = self.service.checkout_loan(patron_id=10, book_item_id=20)

        self.assertIsNotNone(new_loan)
        self.assertEqual(new_loan.patron_id, 10)
        self.assertEqual(new_loan.book_item_id, 20)
        self.assertEqual(new_loan.id, 1)

    def test_checkout_loan_unavailable_book_item(self):
        print("Executando test_checkout_loan_unavailable_book_item...")
        existing_loan = Loan(
            id=99,
            book_item_id=20,
            patron_id=30,
            loan_date=datetime.now() - timedelta(days=1),
            due_date=datetime.now() + timedelta(days=7),
            return_date=None,
        )
        self.mock_repo.get_loans.return_value = [existing_loan]

        new_loan = self.service.checkout_loan(patron_id=10, book_item_id=20)

        self.assertIsNone(new_loan)

if __name__ == "__main__":
    unittest.main()

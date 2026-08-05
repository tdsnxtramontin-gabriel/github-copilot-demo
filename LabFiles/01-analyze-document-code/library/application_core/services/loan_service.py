from ..interfaces.iloan_service import ILoanService
from ..interfaces.iloan_repository import ILoanRepository
from ..entities.loan import Loan
from ..enums.loan_return_status import LoanReturnStatus
from ..enums.loan_extension_status import LoanExtensionStatus
from typing import Optional
from datetime import datetime, timedelta

class LoanService(ILoanService):
    EXTEND_BY_DAYS = 14

    def __init__(self, loan_repository: ILoanRepository):
        self._loan_repository = loan_repository

    def return_loan(self, loan_id: int) -> LoanReturnStatus:
        loan = self._loan_repository.get_loan(loan_id)
        if loan is None:
            return LoanReturnStatus.LOAN_NOT_FOUND
        if loan.return_date is not None:
            return LoanReturnStatus.ALREADY_RETURNED
        loan.return_date = datetime.now()
        try:
            self._loan_repository.update_loan(loan)
            return LoanReturnStatus.SUCCESS
        except Exception:
            return LoanReturnStatus.ERROR

    def extend_loan(self, loan_id: int) -> LoanExtensionStatus:
        loan = self._loan_repository.get_loan(loan_id)
        if loan is None:
            return LoanExtensionStatus.LOAN_NOT_FOUND
        if loan.patron and loan.patron.membership_end < datetime.now():
            return LoanExtensionStatus.MEMBERSHIP_EXPIRED
        if loan.return_date is not None:
            return LoanExtensionStatus.LOAN_RETURNED
        if loan.due_date < datetime.now():
            return LoanExtensionStatus.LOAN_EXPIRED
        try:
            loan.due_date = loan.due_date + timedelta(days=self.EXTEND_BY_DAYS)
            self._loan_repository.update_loan(loan)
            return LoanExtensionStatus.SUCCESS
        except Exception:
            return LoanExtensionStatus.ERROR

    def checkout_loan(self, patron_id: int, book_item_id: int) -> Optional[Loan]:
        loans = self._loan_repository.get_loans()
        has_active_loan = any(
            loan.book_item_id == book_item_id and loan.return_date is None
            for loan in loans
        )
        if has_active_loan:
            return None

        next_id = max((loan.id for loan in loans), default=0) + 1
        now = datetime.now()
        new_loan = Loan(
            id=next_id,
            book_item_id=book_item_id,
            patron_id=patron_id,
            loan_date=now,
            due_date=now + timedelta(days=self.EXTEND_BY_DAYS),
            return_date=None,
        )
        return self._loan_repository.add_loan(new_loan)

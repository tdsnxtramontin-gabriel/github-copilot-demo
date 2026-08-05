from abc import ABC, abstractmethod
from typing import Optional
from ..entities.loan import Loan
from ..enums.loan_return_status import LoanReturnStatus
from ..enums.loan_extension_status import LoanExtensionStatus

class ILoanService(ABC):
    @abstractmethod
    def return_loan(self, loan_id: int) -> LoanReturnStatus:
        pass

    @abstractmethod
    def extend_loan(self, loan_id: int) -> LoanExtensionStatus:
        pass

    @abstractmethod
    def checkout_loan(self, patron_id: int, book_item_id: int) -> Optional[Loan]:
        pass

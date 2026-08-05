from enum import Enum

class LoanReturnStatus(Enum):
    SUCCESS = 'Livro devolvido com sucesso.'
    LOAN_NOT_FOUND = 'Empréstimo não encontrado.'
    ALREADY_RETURNED = 'Não é possível devolver o livro porque ele já foi devolvido.'
    ERROR = 'Não é possível devolver o livro devido a um erro.'

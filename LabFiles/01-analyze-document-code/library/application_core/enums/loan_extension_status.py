from enum import Enum

class LoanExtensionStatus(Enum):
    SUCCESS = 'A extensão do empréstimo do livro foi concluída com sucesso.'
    LOAN_NOT_FOUND = 'Empréstimo não encontrado.'
    LOAN_EXPIRED = 'Não é possível estender o empréstimo do livro porque ele já expirou. Devolva o livro.'
    MEMBERSHIP_EXPIRED = 'Não é possível estender o empréstimo do livro devido à assinatura expirada do leitor.'
    LOAN_RETURNED = 'Não é possível estender o empréstimo do livro porque o livro já foi devolvido.'
    ERROR = 'Não é possível estender o empréstimo do livro devido a um erro.'

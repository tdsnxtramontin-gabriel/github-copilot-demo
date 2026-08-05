from enum import Enum

class MembershipRenewalStatus(Enum):
    SUCCESS = 'A renovação da assinatura foi concluída com sucesso.'
    PATRON_NOT_FOUND = 'Leitor não encontrado.'
    TOO_EARLY_TO_RENEW = 'Ainda é cedo para renovar a assinatura.'
    LOAN_NOT_RETURNED = 'Não é possível renovar a assinatura devido a um empréstimo pendente.'
    ERROR = 'Não é possível renovar a assinatura devido a um erro.'

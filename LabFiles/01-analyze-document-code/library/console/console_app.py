from .console_state import ConsoleState
from .common_actions import CommonActions
from application_core.interfaces.ipatron_repository import IPatronRepository
from application_core.interfaces.iloan_repository import ILoanRepository
from application_core.interfaces.iloan_service import ILoanService
from application_core.interfaces.ipatron_service import IPatronService
from infrastructure.json_data import JsonData

class ConsoleApp:
    def __init__(
        self,
        loan_service: ILoanService,
        patron_service: IPatronService,
        patron_repository: IPatronRepository,
        loan_repository: ILoanRepository,
        json_data: JsonData,
    ):
        self._current_state: ConsoleState = ConsoleState.PATRON_SEARCH
        self.matching_patrons = []
        self.selected_patron_details = None
        self.selected_loan_details = None
        self._patron_repository = patron_repository
        self._loan_repository = loan_repository
        self._loan_service = loan_service
        self._patron_service = patron_service
        self._json_data = json_data
        self._book_search_return_state: ConsoleState = ConsoleState.PATRON_SEARCH

    def _open_book_search(self, return_state: ConsoleState) -> ConsoleState:
        self._book_search_return_state = return_state
        return ConsoleState.BOOK_SEARCH

    def _find_books_by_title(self, title_input: str):
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

    def _choose_book_from_matches(self, matches):
        print("Múltiplos livros correspondem à busca:")
        for idx, book in enumerate(matches, 1):
            print(f"{idx}) {book.title}")

        while True:
            selection = input("Digite um número para escolher, 'r' para refinar, ou 'q' para voltar: ").strip().lower()
            if selection == 'q':
                return None
            if selection == 'r':
                return "REFINE"
            if selection.isdigit():
                idx = int(selection)
                if 1 <= idx <= len(matches):
                    return matches[idx - 1]
            print("Entrada inválida. Tente novamente.")

    def _check_book_availability(self, book):
        related_items = [book_item for book_item in self._json_data.book_items if book_item.book_id == book.id]
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
            key=lambda loan: loan.due_date if loan.due_date is not None else float("inf")
        )
        return False, active_loans_sorted[0] if active_loans_sorted else None, None

    def _prompt_checkout_for_available_book(self, book, available_item) -> None:
        patron = self.selected_patron_details
        if patron is None:
            print("Selecione um leitor antes de realizar um empréstimo.")
            return

        while True:
            choice = input("Digite 's' para emprestar este livro agora ou 'n' para cancelar: ").strip().lower()
            if choice == 'n':
                return
            if choice == 's':
                new_loan = self._loan_service.checkout_loan(patron.id, available_item.id)
                if new_loan is None:
                    print("Não foi possível concluir o empréstimo. O exemplar pode ter sido emprestado agora.")
                    return

                self.selected_loan_details = self._loan_repository.get_loan(new_loan.id)
                self.selected_patron_details = self._patron_repository.get_patron(patron.id)
                print(f"Empréstimo realizado com sucesso para {patron.name}.")
                print(f"Vencimento: {new_loan.due_date}")
                return

            print("Entrada inválida. Digite 's' ou 'n'.")

    def _search_again_or_return(self) -> bool:
        while True:
            choice = input("Digite 's' para buscar novamente ou 'q' para voltar ao menu anterior: ").strip().lower()
            if choice == 's':
                return True
            if choice == 'q':
                return False
            print("Entrada inválida. Digite 's' ou 'q'.")

    def write_input_options(self, options: CommonActions) -> None:
        print("\nOpções de entrada:")
        if options & CommonActions.SELECT:
            print(" - Digite um número para selecionar um leitor da lista")
        if options & CommonActions.RENEW_PATRON_MEMBERSHIP:
            print(" - Digite 'm' para renovar assinatura")
        if options & CommonActions.RETURN_LOANED_BOOK:
            print(" - Digite 'r' para devolver o livro")
        if options & CommonActions.EXTEND_LOANED_BOOK:
            print(" - Digite 'e' para estender o empréstimo")
        if options & CommonActions.SEARCH_BOOKS:
            print(" - Digite 'b' para verificar a disponibilidade de livros")
        if options & CommonActions.SEARCH_PATRONS:
            print(" - Digite 's' para buscar novamente")
        if options & CommonActions.QUIT:
            print(" - Digite 'q' para sair")

    def run(self) -> None:
        while True:
            if self._current_state == ConsoleState.PATRON_SEARCH:
                self._current_state = self.patron_search()
            elif self._current_state == ConsoleState.PATRON_SEARCH_RESULTS:
                self._current_state = self.patron_search_results()
            elif self._current_state == ConsoleState.PATRON_DETAILS:
                self._current_state = self.patron_details()
            elif self._current_state == ConsoleState.LOAN_DETAILS:
                self._current_state = self.loan_details()
            elif self._current_state == ConsoleState.BOOK_SEARCH:
                self._current_state = self.search_books()
            elif self._current_state == ConsoleState.QUIT:
                break

    def patron_search(self) -> ConsoleState:
        search_input = input("Digite um termo para buscar leitores por nome: ").strip()
        if not search_input:
            print("Nenhuma entrada foi informada. Tente novamente.")
            return ConsoleState.PATRON_SEARCH
        self.matching_patrons = self._patron_repository.search_patrons(search_input)
        if not self.matching_patrons:
            print("Nenhum leitor correspondente foi encontrado.")
            return ConsoleState.PATRON_SEARCH
        print("Títulos correspondentes:")
        book_examples = [
            ("Hábitos Atômicos"),
            ("O Poder do Hábito"),
            ("Padrões de Alta Performance"),
            ("Os segredos da Mente Milionária"),
            ("Cabeça de Campeão"),
            ("O Homem Mais Rico da Babilônia"),
            ("Pai Rico, Pai Pobre"),
            ("Arquitetura Limpa"),
            ("Código Limpo"),
            ("Entendendo Algoritmos"),
        ]
        for idx, patron in enumerate(self.matching_patrons, 1):
            title = book_examples[(idx - 1) % len(book_examples)]
            print(f"{idx}) {title}")
        return ConsoleState.PATRON_SEARCH_RESULTS

    def patron_search_results(self) -> ConsoleState:
        self.write_input_options(
            CommonActions.SELECT
            | CommonActions.SEARCH_BOOKS
            | CommonActions.SEARCH_PATRONS
            | CommonActions.QUIT
        )
        selection = input("Digite sua escolha: ").strip().lower()
        if selection == 'q':
            return ConsoleState.QUIT
        elif selection == 's':
            return ConsoleState.PATRON_SEARCH
        elif selection == 'b':
            return self._open_book_search(ConsoleState.PATRON_SEARCH_RESULTS)
        elif selection.isdigit():
            idx = int(selection)
            if 1 <= idx <= len(self.matching_patrons):
                self.selected_patron_details = self.matching_patrons[idx - 1]
                return ConsoleState.PATRON_DETAILS
            else:
                print("Seleção inválida. Digite um número válido.")
                return ConsoleState.PATRON_SEARCH_RESULTS
        else:
            print("Entrada inválida. Digite um número, 'b', 's' ou 'q'.")
            return ConsoleState.PATRON_SEARCH_RESULTS

    def patron_details(self) -> ConsoleState:
        patron = self.selected_patron_details
        print(f"\nNome: {patron.name}")
        print(f"Expiração da assinatura: {patron.membership_end}")
        loans = self._loan_repository.get_loans_by_patron_id(patron.id)
        print("\nEmpréstimos de livros:")

        # Filtra e exibe empréstimos válidos.
        valid_loans = []
        for idx, loan in enumerate(loans, 1):
            if not getattr(loan, 'book_item', None) or not getattr(loan.book_item, 'book', None):
                print(f"{idx}) [Dados de empréstimo inválidos: faltam informações do livro]")
            else:
                returned = "Sim" if getattr(loan, 'return_date', None) else "Não"
                print(f"{idx}) {loan.book_item.book.title} - Vencimento: {loan.due_date} - Devolvido: {returned}")
                valid_loans.append((idx, loan))
        if valid_loans:
            print("Digite um número para selecionar um empréstimo da lista")
        if not valid_loans:
            print("Não há empréstimos válidos para este leitor.")
            self.write_input_options(
                CommonActions.SEARCH_BOOKS
                | CommonActions.SEARCH_PATRONS
                | CommonActions.QUIT
            )
            selection = input("Digite sua escolha: ").strip().lower()
            if selection == 'q':
                return ConsoleState.QUIT
            elif selection == 's':
                return ConsoleState.PATRON_SEARCH
            elif selection == 'b':
                return self._open_book_search(ConsoleState.PATRON_DETAILS)
            else:
                print("Entrada inválida.")
                return ConsoleState.PATRON_DETAILS
        else:
            self.write_input_options(
                CommonActions.SELECT
                | CommonActions.RENEW_PATRON_MEMBERSHIP
                | CommonActions.SEARCH_BOOKS
                | CommonActions.SEARCH_PATRONS
                | CommonActions.QUIT
            )
            selection = input("Digite sua escolha: ").strip().lower()
            if selection == 'q':
                return ConsoleState.QUIT
            elif selection == 's':
                return ConsoleState.PATRON_SEARCH
            elif selection == 'b':
                return self._open_book_search(ConsoleState.PATRON_DETAILS)
            elif selection == 'm':
                status = self._patron_service.renew_membership(patron.id)
                print(status)
                self.selected_patron_details = self._patron_repository.get_patron(patron.id)
                return ConsoleState.PATRON_DETAILS
            elif selection.isdigit():
                idx = int(selection)
                if 1 <= idx <= len(valid_loans):
                    self.selected_loan_details = valid_loans[idx - 1][1]
                    return ConsoleState.LOAN_DETAILS
                print("Seleção inválida. Digite um número exibido na lista acima.")
                return ConsoleState.PATRON_DETAILS
            else:
                print("Entrada inválida. Digite um número, 'm', 'b', 's' ou 'q'.")
                return ConsoleState.PATRON_DETAILS

    def loan_details(self) -> ConsoleState:
        loan = self.selected_loan_details
        print(f"Título do livro: {loan.book_item.book.title}")
        print(f"Autor do livro: {loan.book_item.book.author.name}")
        print(f"Data de vencimento: {loan.due_date}")
        returned = "Sim" if getattr(loan, 'return_date', None) else "Não"
        print(f"Devolvido: {returned}\n")
        self.write_input_options(
            CommonActions.RETURN_LOANED_BOOK
            | CommonActions.EXTEND_LOANED_BOOK
            | CommonActions.SEARCH_PATRONS
            | CommonActions.QUIT
        )
        selection = input("Digite sua escolha: ").strip().lower()
        if selection == 'q':
            return ConsoleState.QUIT
        elif selection == 's':
            return ConsoleState.PATRON_SEARCH
        elif selection == 'r':
            status = self._loan_service.return_loan(loan.id)
            print("Livro devolvido com sucesso.")
            print(status)
            self.selected_loan_details = self._loan_repository.get_loan(loan.id)
            return ConsoleState.LOAN_DETAILS
        elif selection == 'e':
            status = self._loan_service.extend_loan(loan.id)
            print(status)
            self.selected_loan_details = self._loan_repository.get_loan(loan.id)
            return ConsoleState.LOAN_DETAILS
        else:
            print("Entrada inválida.")
            return ConsoleState.LOAN_DETAILS

    def search_books(self) -> ConsoleState:
        while True:
            book_title = input("Digite o título de um livro para buscar: ").strip()
            if not book_title:
                print("Nenhuma entrada foi informada. Tente novamente.")
                if self._search_again_or_return():
                    continue
                return self._book_search_return_state

            matches = self._find_books_by_title(book_title)
            if not matches:
                print("Nenhum livro correspondente foi encontrado.")
                if self._search_again_or_return():
                    continue
                return self._book_search_return_state

            if len(matches) > 1:
                chosen = self._choose_book_from_matches(matches)
                if chosen is None:
                    return self._book_search_return_state
                if chosen == "REFINE":
                    continue
                book = chosen
            else:
                book = matches[0]

            is_available, blocking_loan, available_item = self._check_book_availability(book)
            if is_available:
                print(f"{book.title} está disponível para empréstimo.")
                self._prompt_checkout_for_available_book(book, available_item)
            else:
                if blocking_loan and blocking_loan.due_date is not None:
                    print(f"{book.title} está emprestado para outro leitor. A data de devolução é {blocking_loan.due_date}.")
                else:
                    print(f"{book.title} está emprestado para outro leitor. A data de devolução não está disponível.")

            if self._search_again_or_return():
                continue
            return self._book_search_return_state
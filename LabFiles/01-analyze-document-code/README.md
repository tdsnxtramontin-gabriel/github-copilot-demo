# Aplicativo da Biblioteca

## Descrição
Aplicativo da Biblioteca é uma aplicação de console em Python para gerenciar operações de biblioteca, como navegação no catálogo, atividade da conta de leitores e processamento de empréstimos. O projeto é organizado com uma arquitetura em camadas que separa a lógica de domínio, as preocupações de infraestrutura, a interação com o usuário e os testes.

## Estrutura do Projeto
- README.md
- requirements.txt
- library/
   - application_core/
      - entities/
         - author.py
         - book.py
         - book_item.py
         - loan.py
         - patron.py
      - enums/
         - loan_extension_status.py
         - loan_return_status.py
         - membership_renewal_status.py
      - interfaces/
         - iloan_repository.py
         - iloan_service.py
         - ipatron_repository.py
         - ipatron_service.py
      - services/
         - loan_service.py
         - patron_service.py
   - console/
      - common_actions.py
      - console_app.py
      - console_state.py
      - main.py
   - infrastructure/
      - Json/
         - Authors.json
         - BookItems.json
         - Books.json
         - Loans.json
         - Patrons.json
      - json_data.py
      - json_loan_repository.py
      - json_patron_repository.py
   - tests/
      - test_loan_service.py
      - test_patron_service.py

## Principais Classes e Interfaces
- Entidades de domínio:
   - `Author`, `Book`, `BookItem`, `Loan` e `Patron` em `library/application_core/entities` modelam o domínio central da biblioteca.
- Interfaces de serviço:
   - `ILoanService` e `IPatronService` definem os contratos de serviço em `library/application_core/interfaces`.
- Interfaces de repositório:
   - `ILoanRepository` e `IPatronRepository` definem os contratos de persistência em `library/application_core/interfaces`.
- Serviços de negócio:
   - `LoanService` e `PatronService` em `library/application_core/services` implementam os principais casos de uso.
- Repositórios de infraestrutura:
   - As implementações de repositório baseadas em JSON em `library/infrastructure` fornecem acesso aos dados.
- Ponto de entrada do console:
   - `library/console/main.py` inicia o fluxo interativo do console.

## Licença
Este projeto é fornecido para fins educacionais e de treinamento.
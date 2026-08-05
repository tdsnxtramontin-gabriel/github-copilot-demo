# Library App

## Description
Library App is a Python-based console application for managing library operations such as catalog browsing, patron account activity, and loan processing. The project is organized with a layered architecture that separates domain logic, infrastructure concerns, user interaction, and tests.

## Project Structure
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

## Key Classes and Interfaces
- Domain entities:
   - `Author`, `Book`, `BookItem`, `Loan`, and `Patron` in `library/application_core/entities` model the core library domain.
- Service interfaces:
   - `ILoanService` and `IPatronService` define service-level contracts in `library/application_core/interfaces`.
- Repository interfaces:
   - `ILoanRepository` and `IPatronRepository` define persistence contracts in `library/application_core/interfaces`.
- Business services:
   - `LoanService` and `PatronService` in `library/application_core/services` implement core use cases.
- Infrastructure repositories:
   - JSON-backed repository implementations in `library/infrastructure` provide data access.
- Console entry point:
   - `library/console/main.py` starts the interactive console workflow.

## License
This project is provided for educational and training purposes.

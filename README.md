## Invoice Manager Backend API

A RESTful API built with Django REST Framework to manage invoices and their details.

### Overview

The API provides endpoints to manage invoices and their details. It allows for creating, retrieving, updating, and deleting invoices and their details. The data is stored in a SQLite database, and Django Rest Framework is used to handle HTTP requests and responses.

### Features
- Create, retrieve, update, and delete invoices.
- Update and delete invoice details.
- Custom Response format for better error handling.
- Comprehensive test suite using rest_framework.test.APITestCase to ensure code quality and functionality.
- Pagination for listing invoices.
- Search and sort functionality for listing invoices.

### Getting Started

1. Clone the repository.
```bash
git clone https://github.com/lordgrim18/invoice-manager.git
```

2. Change into the project directory.
```bash
cd invoice-manager
```

3. Create a virtual environment and activate it.
```bash
python -m venv venv
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Install the project dependencies.
```bash
pip install -r requirements.txt
```

5. Initialize the sqlite database
```bash
python .\db-scripts\create_tables.py
```
Note:
In case you want some dummy data to fill the database run the following line in the terminal
```bash
python .\db-scripts\insert_dummy_data.py
```

6. Run the development server.
```bash
python manage.py runserver
```

warning : ensure that you do not make migrations to the database, as we have disabled admin and similar features.

6. The API will be available at `http://localhost:8000/`.

### Testing

Tests for the API endpoints have been written using Django's `APITestCase` from `rest_framework.test`. These tests ensure that the API functions correctly and handles various scenarios effectively.

Run the test suite to ensure everything is working as expected.
```bash
python manage.py test
```

### Endpoints

The API provides the following endpoints:

- **Create Invoice**: `POST /invoice/create/`
- **List Invoices**: `GET /invoice/`
- **Update Invoice**: `PUT /invoice/update/<invoice_id>/`
- **Partial Update Invoice**: `PATCH /invoice/partial-update/<invoice_id>/`
- **Delete Invoice**: `DELETE /invoice/delete/<invoice_id>/`
- **View Single Invoice**: `GET /invoice/get/<invoice_id>/`
- **Partial Update Invoice Detail**: `PATCH /invoice-detail/partial-update/<invoice_detail_id>/`
- **Delete Invoice Detail**: `DELETE /invoice-detail/delete/<invoice_detail_id>/`
- **Create Invoice Detail**: `POST /invoice-detail/create/<invoice_id>/`
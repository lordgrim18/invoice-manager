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

5. Create a `.env` file in the root of the project to add the environment variables for the project. 
The environment variables that are needed are given in the `.env.sample` file. 
```bash
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
```

- Here, secret key is the Django secret key for the project. You can generate a new secret key using the following command in your terminal.
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

- The `DEBUG` variable is used to enable or disable the debug mode for the project. This allows for better error handling and debugging. `DEBUG` should be set to `True` for development and `False` for production.
- The `ALLOWED_HOSTS` variable is used to specify the hosts that are allowed to make requests to the project. This can be set to `*` to allow all hosts. 


6. Initialize the sqlite database
```bash
python .\db-scripts\create_tables.py
```
Note:
In case you want some dummy data to fill the database run the following line in the terminal
```bash
python .\db-scripts\insert_dummy_data.py
```

7. Run the development server.
```bash
python manage.py runserver
```

warning : ensure that you do not make migrations to the database, as we have disabled admin and similar features.

8. The API will be available at `http://localhost:8000/`.

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
- **List Invoices Minimal**: `GET /invoice/get/minimal/`
- 
- **View Single Invoice**: `GET /invoice/get/<invoice_id>/`
- **Update Invoice**: `PUT /invoice/update/<invoice_id>/`
- **Partial Update Invoice**: `PATCH /invoice/partial-update/<invoice_id>/`
- **Delete Invoice**: `DELETE /invoice/delete/<invoice_id>/`
- 
- **Partial Update Invoice Detail**: `PATCH /invoice-detail/partial-update/<invoice_detail_id>/`
- **Delete Invoice Detail**: `DELETE /invoice-detail/delete/<invoice_detail_id>/`
- **Create Invoice Detail**: `POST /invoice-detail/create/<invoice_id>/`

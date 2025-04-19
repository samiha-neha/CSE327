# Hut Bazaar

Hut Bazaar is a Django-based web application for grocery shopping. It consists of features like showing items in home page, cart system, review system, order system, email system, wishlist system, admin panel and much more. This repository contains the source code, tests, and documentation for the project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting Up the Environment](#setting-up-the-environment)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [Generating Documentation](#generating-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites
Before setting up the project, ensure you have the following installed:
- **Python 3.12** (recommended, as the project was developed with Anaconda’s Python 3.12)
- **Conda** (for managing the virtual environment)
- **Git** (for cloning the repository)
- A code editor like **VS Code** (optional, but recommended)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/CSE327.git
   cd hut_bazaar
   ```

2. **Verify Project Structure**:
   The project should have the following structure:
   ```
   hut_bazaar/
   ├── hut_bazaar/
   │   ├── __init__.py
   │   ├── checkout/
   │   │   ├── __init__.py
   │   │   ├── tests.py
   │   ├── settings.py
   │   ├── urls.py
   │   ├── wsgi.py
   ├── manage.py
   ├── requirements.txt
   ├── README.md
   ```
   Ensure `__init__.py` files exist in `hut_bazaar/` and `hut_bazaar/checkout/` to make them Python packages.

## Setting Up the Environment
The project uses a Conda environment to manage dependencies. Follow these steps to set up the environment:

1. **Create a Conda Environment**:
   ```bash
   python3 -m venv env
   ```

2. **Activate the Environment**:
   ```bash
   source env/bin/activate
   ```

3. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install django sphinx reportlab python-dotenv
   ```
   

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root (`hut_bazaar/`) to store sensitive settings (e.g., `SECRET_KEY`, database credentials).
   - Example `.env`:
     ```
     SECRET_KEY=your-secret-key
     DEBUG=True
     DATABASE_URL=sqlite:///db.sqlite3
     ```
   - Ensure `python-dotenv` is installed to load these variables in `settings.py`.

5. **Update `manage.py`**:
   Ensure `manage.py` includes the project root in the Python path to resolve module imports:
   ```python
   import os
   import sys
   sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

   def main():
       os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hut_bazaar.settings')
       try:
           from django.core.management import execute_from_command_line
       except ImportError as exc:
           raise ImportError(
               "Couldn't import Django. Are you sure it's installed and "
               "available on your PYTHONPATH environment variable? Did you "
               "forget to activate a virtual environment?"
           ) from exc
       execute_from_command_line(sys.argv)

   if __name__ == '__main__':
       main()
   ```

6. **Apply Migrations**:
   Initialize the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Running the Project
1. **Activate the Conda Environment**:
   ```bash
   source env/bin/activate
   ```

2. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   - Open your browser and navigate to `http://127.0.0.1:8000/` to view the application.

3. **Create a Superuser (Optional)**:
   To access the Django admin interface, create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
   - Log in at `http://127.0.0.1:8000/admin`.

## Running Tests
The project includes tests located in `hut_bazaar/checkout/tests.py`. To run the tests:
1. **Activate the Environment**:
   ```bash
   conda activate hut_bazaar_env
   ```

2. **Run Tests**:
   ```bash
   python manage.py test hut_bazaar.checkout.tests -v 2
   ```
   - The `-v 2` flag provides verbose output for debugging.

3. **Clear Cache (if needed)**:
   If tests fail due to stale cache, clear Python’s compiled files:
   ```bash
   find . -name "__pycache__" -exec rm -rf {} +
   find . -name "*.pyc" -exec rm -f {} +
   ```

## Generating Documentation
The project uses **Sphinx** for documentation. To generate and view the docs:
1. **Navigate to the Docs Directory**:
   If a `docs/` directory exists, navigate to it:
   ```bash
   cd docs
   ```
   If not, initialize Sphinx:
   ```bash
   mkdir docs
   cd docs
   sphinx-quickstart
   ```

2. **Build Documentation**:
   ```bash
   make html
   ```
   - The generated HTML files will be in `docs/_build/html/`.

3. **View Documentation**:
   Open `docs/_build/html/index.html` in a browser.

## Troubleshooting
- **ModuleNotFoundError: No module named 'hut_bazaar.checkout'**:
  - Ensure `__init__.py` files exist in `hut_bazaar/` and `hut_bazaar/checkout/`.
  - Verify the project root is in the Python path (see `manage.py` modification).
  - Check case sensitivity (e.g., `hut_bazaar` vs. `hut_bazaar`).
  - Run:
    ```bash
    python
    >>> import sys
    >>> sys.path.append('/path/to/hut_bazaar')
    >>> import hut_bazaar.checkout.tests
    ```

- **ModuleNotFoundError: No module named 'django'**:
  - Ensure Django is installed in the active Conda environment:
    ```bash
    pip install django
    ```

- **Tests Not Found**:
  - Use the correct test path: `hut_bazaar.checkout.tests`.
  - Verify `tests.py` contains valid Django test cases (e.g., subclasses of `django.test.TestCase`).

- **Environment Issues**:
  - List Conda environments:
    ```bash
    conda env list
    ```
  - Activate the correct environment and reinstall dependencies if needed.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

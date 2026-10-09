# Baby Tools World

This repository contains the source code of 'Baby Tools World', a simple online shop for baby products.
Visitors can browse products by category, read and write reviews, and see tags that describe each product.
Shop owners manage products, categories, and tags in an admin panel.
The project was developed for educational purposes only and therefore makes no claim to feature completeness, application security, user experience, or design.

> [!NOTE]
> This project assumes you already know the Python programming language.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Project Structure](#project-structure)
  - [Apps Overview](#apps-overview)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Managing product tags](#managing-product-tags)
  - [Writing reviews](#writing-reviews)
  - [Seeding the application with data](#seeding-the-application-with-data)
  - [Running the linting tools](#running-the-linting-tools)
  - [Testing](#testing)
  - [Running with a WSGI Server](#running-with-a-wsgi-server)
  - [Containerization](#containerization)

## Features

- **Products and categories**: products are grouped into categories. Visitors can browse the product list, filter it by category, and open a detail page for each product.
- **Product detail page**: shows the product information, a rating summary, the product tags, and the customer reviews.
- **Product tags**: products can have one or more optional tags (e.g. type or age group). Tags are managed in the admin panel and shown on the product detail page. See [Managing product tags](#managing-product-tags).
- **Reviews**: visitors and logged-in users can rate a product with stars and write a comment. Logged-in users have one review per product, which is updated when they send a new one. See [Writing reviews](#writing-reviews).
- **User accounts**: users can register, log in, and log out.
- **Admin panel**: shop owners manage products, categories, and tags, and can filter products by tag.
- **Example data**: the `seed_db` command fills the database with example categories and products.
- **Container support**: the application can be built and run as a Docker image.

## Prerequisites

To work with the repository and the software it contains, you need the following tools installed:

- Python 3.12 or newer
- Git
- An OCI-compliant container engine (e.g. Docker or Podman), only needed for running the app in a container
- An editor or IDE of your choice (VS Code, PyCharm, etc.)

## Quickstart

To get the application running quickly, follow these steps:

1. Clone the repository:
   `git clone <repository-url>`
2. Navigate to the repository:
   `cd baby-tools`
3. Create a virtual environment:
   `python -m venv venv`
4. Activate the virtual environment:
   - on Windows run: `venv\Scripts\activate`
   - on macOS/Linux run: `source venv/bin/activate`
5. Install the project dependencies:
   `pip install -r requirements.txt`
6. Create your environment file from the example (in the root directory of the repository):
   `cp example.env .env`
7. Go to the `src` directory:
   `cd src`
8. Apply the database migrations:
   `python manage.py migrate`
9. (Optional) Fill the database with example categories and products:
   `python manage.py seed_db`
10. (Optional) Create an admin user:
    `python manage.py createsuperuser`
11. Start the application:
    `python manage.py runserver`
12. Open `http://localhost:8000` in your browser to check that the application is running.

## Project Structure

- `.github`: GitHub-specific project files, e.g. the CI workflows
- `.gitlab`: GitLab-specific project files
- `docs`: additional documentation
- `src`: application source code, containing the Django project, apps, and other files
- `requirements.txt`: the project dependencies with pinned versions
- `pyproject.toml`: configuration for the code-quality tools (black, isort, flake8)

### Apps Overview

The project is split into several apps:

- `products`: manages products, categories, tags, and customer reviews
- `users`: handles user registration, login, and logout

Each app has its own `models.py`, `views.py`, `urls.py`, and `admin.py` files to encapsulate its functionality.

## Usage

This section describes the project in more detail.

### Configuration

The application reads its settings from environment variables, which are stored in a `.env` file.

1. Copy the example environment file in the root directory of the repository:
    `cp example.env .env`
    - The file must be stored in the root directory of the repository, next to this README.
    - The `.env` file contains secrets and is ignored by Git. Never commit it.
2. Open `.env` and set the environment variables:
    - `SECRET_KEY`: a long random string. It is required when `DEBUG` is `false`.
      If it is missing while `DEBUG` is `true`, a temporary key is generated automatically.
      You can generate a key with:
      `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
    - `DEBUG`: `true` for development or `false` for production. Use lowercase letters. Defaults to `true`.
    - `ALLOWED_HOSTS`: a comma-separated list of allowed host names. Defaults to `localhost, 127.0.0.1, 0.0.0.0`.
    - `AUTHOR`: the name that is shown in the footer of the application.

### Managing product tags

Tags help to group products, for example by type or age group.

1. Create an admin user with `python manage.py createsuperuser`, if you have not done this yet.
2. Open `http://localhost:8000/admin` and log in.
3. Under **Products → Tags**, create new tags.
4. Open a product and select one or more tags. Tags are optional, so a product can also have no tags.
5. In the product list of the admin panel, use the **filter** on the right side to show only products with a certain tag.

On the product detail page, the tags are shown under the rating summary in the section **Product-Tags**.
If a product has no tags, the page shows "no tags available".

### Writing reviews

Every product page contains a review form with a star rating and an optional comment.

- Visitors who are not logged in must enter their name and email address.
- Logged-in users can write one review per product. If they send a new review, their previous review is updated.
- After a review was sent successfully, the form is cleared.

### Seeding the application with data

To fill the database with some example categories and products, run the management command `seed_db`.
Run it in the directory where the `manage.py` file is stored:

```bash
python manage.py seed_db
```

### Running the linting tools

> [!TIP]
> The required packages are installed with `pip install -r requirements.txt`.
> If you use a virtual environment, it must be activated.

To check and fix the code style and formatting, run the following commands in the root directory of the repository:

```bash
# format the Python code
black .
# sort the imports
isort .
# check the code style
flake8
```

#### When to run this

Check the code style before you push your commits to the remote repository.
If a rule is violated, the CI workflow fails. In that case, run the linting tools, commit the changes, push them, and check if the pipeline passes.

> [!NOTE]
> If a CI workflow fails, check its logs to find out which step failed and why.

### Testing

This project contains tests for its apps.
Tests in Django can be located in a `tests.py` file within an app, or in a `tests` module (a folder with an `__init__.py` file).

> [!TIP]
> By default, the Django test runner finds all Python files whose name starts with `test`, e.g. `test_views.py`.

Example structure:

```console
baby-tools/src/products
├───management
├───migrations
├───templates
└───tests                       <-- this is the module
      ├───__init__.py
      ├───test_category_model.py  <-- this is a test file
      └───test_product_model.py   <-- this is a test file too
```

#### Running tests

To run the tests, use the following command in the `src` directory (where `manage.py` is stored):

```bash
python manage.py test
```

To also measure the test coverage, run:

```bash
coverage run --branch --omit=manage.py,test*.py manage.py test
coverage report
```

For more information about testing, see the [testing documentation](./docs/testing.md).

### Running with a WSGI Server

**WSGI** (Web Server Gateway Interface) is a standard interface between web servers and Python web applications.
It allows web servers to communicate with Python applications in a consistent way.

In a production environment, a WSGI server such as Gunicorn forwards requests to the Django application and returns the responses to the client.
This lets the application handle HTTP requests efficiently and reliably.

> `gunicorn` and `waitress` can be used for the same purpose.
> Running `gunicorn` on Windows can cause problems, which can be avoided by using `waitress` instead.
>
> See the following [quote](https://docs.gunicorn.org/en/stable/index.html) from the official Gunicorn website:
>> Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

For more information about WSGI and its configuration, see the [WSGI documentation](./docs/wsgi.md).

### Containerization

This section explains how to run the application in a container.

> [!NOTE]
> This guide uses Docker. For other OCI-compliant tools such as Podman, the commands are very similar.

#### Build an image

Run the following command in the root directory of the repository:

```bash
# -t sets the image name and tag
# -> baby-tools-world is the image name, local is the tag
docker build -t baby-tools-world:local .
```

#### Run a container

To start a container based on the image, run:

```bash
docker run --rm -it -p 8000:8000 baby-tools-world:local
```

To use your own environment configuration, pass your `.env` file to the container:

```bash
docker run --rm -it -p 8000:8000 --env-file .env baby-tools-world:local
```

Then open `http://localhost:8000` in your browser.

> [!IMPORTANT]
> If you set `DEBUG=false`, you must also set a `SECRET_KEY` in the `.env` file. Otherwise, the application does not start.
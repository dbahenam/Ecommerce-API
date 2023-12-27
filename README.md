# DRF Ecommerce API

## Overview

This project lays the groundwork for a future comprehensive ecommerce website. It establishes an API that will be utilized by the frontend to populate an ecommerce store with products, brands, and categories. The API provides detailed access to product information, including images, stock quantities, SKU numbers, and product lines. A notable feature is the use of Django MPTT to create a hierarchical structure for categories, allowing for relationships like 'clothes' as a parent category and 'shoes' as a child category.

## Key Features

- Access to product information, brand details, and categories.
- Hierarchical category structure using Django MPTT.
- Product details including images, stock quantities, and SKU numbers.

## Technology Stack

- Python 3.9.6
- Django 4.2.6
- Django REST Framework (DRF) 3.14.0
- Pytest 7.4.2
- Django MPTT 0.14.0

## Setup and Installation

1. Ensure Python and PIP are installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the project directory and run **pip install -r requirements.txt** to install dependencies.
4. Set up the database by running **python manage.py makemigrations** followed by **python manage.py migrate**.

## Running the Application

1. Start the Django development server using **python manage.py runserver**.
2. Access the API locally at **'http://127.0.0.1:8000/api'**.

## Testing

- Run tests using the command **pytest** in the terminal within the project directory.
- Generate a coverage report by running **coverage html**.

## API Documentation

Interactive API documentation is available at **'http://127.0.0.1:8000/api/schema/docs'**, powered by DRF Spectacular.

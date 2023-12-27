# DRF Ecommerce API

## Overview

This project establishes the foundation for a future, comprehensive ecommerce website by developing an API that serves as a backbone for the frontend. It enables the presentation of a rich and dynamic ecommerce store, complete with a diverse range of products, brands, and hierarchical categories. Utilizing Django MPTT, the API adeptly handles complex category structures, such as nesting 'shoes' under a 'clothes' parent category. The introduction of Attribute, AttributeValue, and ProductType models significantly enriches product descriptions, offering a detailed and organized portrayal of product characteristics.

## Key Features

- Detailed Product Information: Provides extensive details about products, including images, stock quantities, SKU numbers, and diverse product lines.
- Hierarchical Category Management: Employs Django MPTT for effective handling of nested categories, enhancing the browsing experience.
- Enhanced Product Descriptions: Incorporates Attribute, AttributeValue, and ProductType models to deliver a comprehensive and structured description of products, catering to various product specifications and types.
- Admin Interface Optimization: Significantly improves the efficiency of the Django admin interface. Features include:
  - Inlines for Product Management: Allows for the seamless creation and management of ProductLines within Product entries, streamlining the product setup process.
  - Attribute Association with Product Types: Facilitates the assignment of specific attributes to product types through inlines, making the process of categorizing and detailing products more intuitive and efficient.
  - Efficient Product Line Creation: Enhances the creation process of product lines, enabling a faster and more efficient management experience.

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

"""
Specific to pytest. This file will be automatically recognized by pytest.
Any fixtures defined within here will be made available to the test files
without needing to be imported. 
"""
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
    CategoryFactory,
    BrandFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory,
)


register(CategoryFactory)  # access as category_factory
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)


"""
A Python class that acts as a dummy web browser, allowing us to test our endpoints.
From Djangos documentation: 
    The test client does not require the web server to be running. 
    In fact, it will run just fine with no web server running at all!
    That is because it avoids the overhead of HTTP and deals directly with the Django framework. 
    This helps make the unit tests run quickly.

    The test client is not capable of retrieving web pages that are not powered by your Django project.
"""


@pytest.fixture
def api_client_callable():
    return APIClient

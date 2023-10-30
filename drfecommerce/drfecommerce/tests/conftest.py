import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import CategoryFactory, BrandFactory, ProductFactory, ProductLineFactory


register(CategoryFactory) # access as category_factory
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)

@pytest.fixture
def api_client_callable():
    return APIClient
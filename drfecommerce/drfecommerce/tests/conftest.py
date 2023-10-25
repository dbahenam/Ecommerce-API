from pytest_factoryboy import register

from .factories import CategoryFactory, BrandFactory, ProductFactory

register(CategoryFactory) # access as category_factory
register(BrandFactory)
register(ProductFactory)
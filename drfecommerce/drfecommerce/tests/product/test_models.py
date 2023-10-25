import pytest

pytestmark = pytest.mark.django_db # access to test database


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        # Act
        x = category_factory(name="test_category")
        # Assert
        assert x.__str__() == "test_category"

class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange
        # Act
        y = brand_factory(name="the_brand")
        # Assert
        assert y.__str__() == "the_brand"

class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        # Act
        y = product_factory(name="test_product")
        # Assert
        assert y.__str__() == "test_product"
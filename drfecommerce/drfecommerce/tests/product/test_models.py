import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db  # access to test database


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange -- bring in resources
        # Act -- perform action
        x = category_factory(name="test_category")
        # Assert -- test
        assert x.__str__() == "test_category"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # Arrange
        # Act
        x = brand_factory(name="the_brand")
        # Assert
        assert x.__str__() == "the_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        # Arrange
        # Act
        x = product_factory(name="test_product")
        # Assert
        assert x.__str__() == "test_product"


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        # Arrange
        # Act
        x = product_line_factory()
        # Assert
        assert x.__str__() == "12345"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        prod_obj = product_factory()  # Create Product object
        product_line_factory(order=1, product=prod_obj)  # Create ProductLine obj
        # check validationerror is raised, order value must be unique
        with pytest.raises(ValidationError):
            product_line_factory(
                order=1, product=prod_obj
            ).clean()  # Create obj with duplicate order value


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        product_image_obj = product_image_factory(url="test_image")
        assert product_image_obj.__str__() == "test_image"

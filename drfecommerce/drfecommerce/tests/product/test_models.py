import pytest
from django.core.exceptions import ValidationError
from drfecommerce.apps.product import models

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


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        # Arrange
        # Act
        x = product_line_factory()
        # Assert
        assert x.__str__() == "test_product_line"


class TestProductModel:
    def test_str_method(self, product_factory, attribute_value_factory):
        # Arrange
        # Act
        x = product_factory()
        # Assert
        assert x.__str__() == "test_product_line-SKU_Number: 12345"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        prod_line_obj = product_line_factory()  # Create Product_Line object
        product_factory(order=1, product_line=prod_line_obj)  # Create Product obj
        # check validationerror is raised, order value must be unique
        with pytest.raises(ValidationError):
            product_factory(order=1, product_line=prod_line_obj)

    def test_attribute_value_mtm(self, product_factory, attribute_value_factory):
        attribute_value_objs = attribute_value_factory.create_batch(3)
        product_factory(attribute_value=(attribute_value_objs))
        x = models.AttributeValue.objects.get(id=1)
        print("x:", x)
        pass


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        product_image_obj = product_image_factory(url="test_image")
        assert product_image_obj.__str__() == "test_image"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        pass

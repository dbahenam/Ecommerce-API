from unicodedata import category
import pytest
import json

from drfecommerce.tests.factories import CategoryFactory, ProductFactory 

pytestmark = pytest.mark.django_db # access to test database


class TestCategoryEndpoints:
    
    endpoint = "/api/category/"

    def test_category_get(self, category_factory, api_client_callable):
        # Arrange
        category_factory.create_batch(5)
        # Act
        response = api_client_callable().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        x = json.loads(response.content)
        print("x is: ", x)
        assert len(json.loads(response.content)) == 5

class TestBrandEndpoints:

   endpoint = "/api/brand/"

   def test_brand_get(self, brand_factory, api_client_callable):
       # Arrange
       brand_factory.create_batch(5)
       # Act
       response = api_client_callable().get(self.endpoint)
       # Assert
       assert response.status_code == 200
       assert len(json.loads(response.content)) == 5

class TestProductEndpoints:

    endpoint = "/api/product/"

    def test_product_get_all(self, product_factory,api_client_callable):
        # Arrange
        product_factory.create_batch(5)
        # Act
        response = api_client_callable().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    def test_product_get_single(self, product_factory, api_client_callable):
        # Arrange
        prod_obj = product_factory.create(slug="product_slug")
        # Act
        response = api_client_callable().get(f"{self.endpoint}{prod_obj.slug}/")
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_product_get_by_category(self, product_factory, api_client_callable):
    # Arrange
        # create a category
        cat_obj = CategoryFactory.create(slug="cat-slug")
        # create a product with that category
        prod_obj = ProductFactory.create(category=cat_obj)
    # Act
        # get product by category slug
        response = api_client_callable().get(f"{self.endpoint}category/{cat_obj.slug}/all/")
    # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
        
class TestProductLineEndpoints:

    endpoint = "/api/product_line/"
    pass

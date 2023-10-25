import pytest
import json 

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

    def test_product_get(self, product_factory,api_client_callable):
        # Arrange
        product_factory.create_batch(5)
        # Act
        response = api_client_callable().get(self.endpoint)
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

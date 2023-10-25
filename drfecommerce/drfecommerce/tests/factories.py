import factory

from drfecommerce.apps.product.models import Category, Brand, Product

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    # name = "test_category"
    name = factory.Sequence(lambda n: "Category_%d" % n)

class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand
    
    name = factory.Sequence(lambda n: "Brand%d" % n)

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = "test_product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
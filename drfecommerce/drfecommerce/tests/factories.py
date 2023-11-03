import factory

from drfecommerce.apps.product.models import (
    Category,
    Brand,
    Product,
    ProductLine,
    ProductImage,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # name = "test_category"
    name = factory.Sequence(lambda n: "Category_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: "Brand_%d" % n)
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 100.00
    sku = "12345"
    stock_qty = 10
    product = factory.SubFactory(ProductFactory)
    is_active = True
    # order should be generated automatically


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test alt text"
    url = "test.jpg"
    productline = factory.SubFactory(ProductLineFactory)

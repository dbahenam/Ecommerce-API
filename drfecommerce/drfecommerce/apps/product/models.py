from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField

# class ActiveManager(models.Manager):
# def get_queryset(self):
#     return super().get_queryset().filter(is_active=True)


# Instead of creating new manager, add queryset methods to manager
class ActiveQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )  # parent category ("clothes"), subcategory ("shoes")
    slug = models.SlugField(max_length=255)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)  # downloadable
    category = TreeForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    objects = ActiveQuerySet.as_manager()

    # active = ActiveManager()
    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField(validators=[MinValueValidator(0)])
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)

    # Validation requiring multiple fields, e.g product and order
    def clean(self, exclude=None):
        super().clean_fields(exclude=exclude)
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:  # Duplicate
                raise ValidationError(
                    "Order value already exists for another product line item."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="productline", blank=True)

    # Validation requiring multiple fields, e.g productline and order
    def clean(self, exclude=None):
        super().clean_fields(exclude=exclude)
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:  # Duplicate
                raise ValidationError(
                    "Order value already exists for another product line item."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

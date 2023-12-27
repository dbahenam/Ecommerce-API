from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


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


class ProductLine(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    category = TreeForeignKey(  # Sets up many-to-many also
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT, related_name="product_line"
    )
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=255)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )

    def __str__(self):
        return f"{self.attribute.name}-{self.value}"


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    attribute = models.ManyToManyField(
        Attribute, through="ProductTypeAttribute", related_name="product_type"
    )

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,  # related_name="product_type_attribute_pt"
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,  # related_name="product_type_attribute_att"
    )

    class Meta:
        unique_together = ["product_type", "attribute"]


class Product(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField(validators=[MinValueValidator(0)])
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product"
    )
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product_line", blank=True)
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductAttributeValue",
        related_name="product",
    )

    def clean(self):
        # Get all products related to a specific product line
        qs = Product.objects.filter(product_line=self.product_line)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:  # Duplicate
                raise ValidationError(
                    "Order value already exists for another product item."
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # ensure clean method is run however data is inserted
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_line.name}-SKU_Number: {str(self.sku)}"


class ProductAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        # related_name="product_attribute_value_av",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        # related_name="product_attribute_value_pl",
    )

    class Meta:
        unique_together = ["attribute_value", "product"]

    def clean(self):
        # check if the entry is a new record, doesn't exists, i.e need validation
        qs_exists = (
            ProductAttributeValue.objects.filter(attribute_value=self.attribute_value)
            .filter(product=self.product)
            .exists()
        )
        if not qs_exists:
            # access attributes associated with product objects by using reverse foreign key
            attribute_objs = Attribute.objects.filter(
                attribute_value__product=self.product
            ).values_list("pk", flat=True)

            if self.attribute_value.attribute.id in list(attribute_objs):
                raise ValidationError("Duplicate Attributes Exists.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductAttributeValue, self).save(*args, **kwargs)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=255)
    url = models.ImageField(upload_to=None, default="test.jpg")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(unique_for_field="product", blank=True)

    # Validation requiring multiple fields, e.g productline and order
    # In order to prevent users from manually entering duplicate numbers
    def clean(self):
        qs = ProductImage.objects.filter(product=self.product)
        for obj in qs:
            if obj.id != self.id and obj.order == self.order:  # Duplicate
                raise ValidationError(
                    "Order value already exists for another product image item."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

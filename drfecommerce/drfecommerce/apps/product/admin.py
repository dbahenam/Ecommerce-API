from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models


# admin.site.register(models.Category)
@admin.register(models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ["name", "slug"]


admin.site.register(models.Brand)


class EditLinkInLine:
    def edit(self, instance):
        url = reverse(
            # admin:product_productline_change
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            return format_html('<a href="{}">Edit</a>', url)
        else:
            return ""

    def add(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_add"
        )
        return format_html('<a href="{}">Add</a>', url)


class ProductImageInLine(admin.TabularInline):
    model = models.ProductImage


class ProductInLine(EditLinkInLine, admin.TabularInline):
    """
    The admin interface has the ability to edit models on the same page as a parent model.
    These are called inlines.

    readonly_fields attribute can accept a list of strings that correspond to:
        Model fields – the actual fields of the model that should be displayed as read-only.
        Method names – the names of methods on the ModelAdmin or InlineModelAdmin that will be called
        to produce the output for a read-only "field" on the admin page.
    """

    model = models.Product
    readonly_fields = ["edit"]


class ProductAttributeValueInLine(admin.TabularInline):
    model = models.ProductAttributeValue


class ProductLineAdmin(admin.ModelAdmin):
    """
    ModelAdmin class is the representation of a model in the admin interface.
    Only create a ModelAdmin object if you are going to customize the representation of a model
    in the admin interface.
    """

    inlines = [ProductInLine]


class AttributeValueInLine(admin.TabularInline):
    model = models.AttributeValue.product.through


class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInLine, ProductImageInLine]


class AttributeInLine(admin.TabularInline):
    model = models.Attribute.product_type.through


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [AttributeInLine]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductLine, ProductLineAdmin)
admin.site.register(models.AttributeValue)
admin.site.register(models.Attribute)
admin.site.register(models.ProductType, ProductTypeAdmin)

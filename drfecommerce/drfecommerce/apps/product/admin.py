from django.contrib import admin
from .models import Category, Brand, Product, ProductLine

class ProductLineInLine(admin.TabularInline):
    model = ProductLine

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInLine,]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)
# admin.site.register(Product, ProductAdmin) also works


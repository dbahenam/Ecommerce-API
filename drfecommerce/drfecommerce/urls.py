from django.contrib import admin
from django.urls import path, include
# DefaultRouter is a class that automatically generates URL patterns for ViewSets
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


from .apps.product import views

router = DefaultRouter()
"""
router will automatically generate CRUD url patterns:
List all categories: GET /api/category/
Create a new category: POST /api/category/
Retrieve a specific category: GET /api/category/{id}/
Update a specific category: PUT /api/category/{id}/
Partially update a specific category: PATCH /api/category/{id}/
Delete a specific category: DELETE /api/category/{id}/
"""
router.register(r'category', views.CategoryViewSet)
router.register(r'brand', views.BrandViewSet)
router.register(r'product', views.ProductViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(),name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views.catalog import ProductViewSet, CategoryViewSet

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
]

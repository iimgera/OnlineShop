from django.urls import path
from api.v1.views.products import ProductListView, CategoryListView


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
]

from rest_framework import generics

from api.v1.serializers.products import CategorySerializer, ProductSerializer
from api.v1.models.products import Category, Product


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

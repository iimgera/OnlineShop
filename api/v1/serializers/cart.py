from rest_framework import serializers
from api.v1.models.cart import Cart
from api.v1.serializers.catalog import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']


class CartGetSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

from rest_framework import serializers
from api.v1.models.orders import Order
from api.v1.serializers.catalog import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

from rest_framework import serializers
from .models import Cart, Item
from ..products.serializers import ProductSerializer


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['quantity', 'product']

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'user',
            'items',
            'total_price',
        ]
        read_only_fields = ('total_price',)


from rest_framework import serializers

from cart.models import Cart
from products.models import Product
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(max_value=10,error_messages={"max_value":"You Can order only 10 per order"})
    product_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = ["user","product","quantity","product_detail"]

    def get_product_detail(self,obj):
        data =  ProductSerializer(instance=Product.objects.get(id=obj.product.id)).data
        data["totalPrice"] = data["price"] * obj.quantity
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

from rest_framework import serializers

from cart.models import Cart
from products.models import Product
from products.serializers import ProductSerializer
from user.models import SiteUser
from user.serializers import SiteUserSerializer


class CartSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(error_messages={"max_value":"You Can order only 10 per order"})
    product_detail = serializers.SerializerMethodField(read_only=True)
    # user = SiteUserSerializer(read_only=True)
    # user_id = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all(),write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.CharField(required=False)
    class Meta:
        model = Cart
        fields = ["user","product","quantity","product_detail","product_id","extra_info"]

    def get_product_detail(self,obj):
        data =  ProductSerializer(instance=Product.objects.get(id=obj.product.id)).data
        data["totalPrice"] = data["price"] * obj.quantity
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
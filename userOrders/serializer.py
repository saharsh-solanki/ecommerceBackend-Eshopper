import json

from rest_framework import serializers, status

from address.models import Address
from address.serializers import AddressSerializer
from cart.models import Cart
from cart.serializer import CartSerializer
from products.models import Product
from products.serializers import ProductSerializer
from user.models import SiteUser
from user.serializers import SiteUserSerializer
from userOrders.models import Orders
from django.http import JsonResponse
from rest_framework.response import Response


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)
    address_id = serializers.CharField(required=False)
    user_id = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all(), write_only=True)
    user = SiteUserSerializer(read_only=True)
    TotalPaidAmount = serializers.FloatField(read_only=True)

    class Meta:
        model = Orders
        fields = [
            "order_id", "products", "address", "address_id",
            "order_date", "paymentType", "user", "user_id",
            "TotalPaidAmount", "status", "discount", "promocode",
            "deliveryStatus", "dehliveryId",
            "transection_id", "id", "cartdata"
        ]

        extra_kwargs = {
            # 'status': {'read_only': True},
            'promocode': {'read_only': True},
            'deliveryStatus': {'read_only': True},
            'dehliveryId': {'read_only': True},
            'transection_id': {'read_only': True},
            'discount': {"read_only": True},
            'id': {"read_only": True}
        }

    # def get_order_id(self, obj):
    #     import random
    #     valid = True
    #     orderId = "None"
    #     while valid == True:
    #         orderId = "ORDER_" + str(random.randint(1000, 1000000000))
    #         if Orders.objects.filter(order_id=orderId).exists():
    #             pass
    #         else:
    #             valid = False
    #     # obj.order_id = orderId
    #     # obj.save()
    #     return orderId

    def create(self, validated_data):
        obj = self.getCart(validated_data["user_id"])
        products = obj["products"]
        cartdata = obj["cartdata"]
        if not products:
            raise serializers.ValidationError("Cart is empty !!", code=status.HTTP_400_BAD_REQUEST)
        totalPaidAmount = obj["total"]
        address = validated_data.pop("address_id")
        user = validated_data.pop("user_id")
        if validated_data["paymentType"] == "COD":
            validated_data['status'] = "SUCCESS"
        # validated_data["order_id"] = self.get_order_id("c")
        # self.order_id =  validated_data["order_id"]
        order = Orders.objects.create(
            address=AddressSerializer(instance=Address.objects.get(id=address)).data,
            products=products, **validated_data, TotalPaidAmount=totalPaidAmount,
            user=user, cartdata=cartdata
        )
        if validated_data["status"] == "SUCCESS":
            self.deleteCart(user)
        return order

    def getCart(self, obj):
        cartdata = Cart.objects.filter(user__email=obj.email)
        CartSerializedData = json.loads(json.dumps(CartSerializer(instance=cartdata, many=True).data))
        amountTotal = 0
        shipping = 49
        products = []
        for cart in cartdata:
            products.append(json.loads(json.dumps(ProductSerializer(instance=cart.product).data)))
            amountTotal = amountTotal + cart.product.price

        return {"products": products, "cartdata": CartSerializedData, "total": amountTotal + shipping}

    def deleteCart(self, obj):
        cartdata = Cart.objects.filter(user__email=obj.email)
        cartdata.delete()

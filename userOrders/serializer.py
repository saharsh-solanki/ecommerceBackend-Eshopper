from rest_framework import serializers, status

from address.models import Address
from address.serializers import AddressSerializer
from cart.models import Cart
from products.models import Product
from products.serializers import ProductSerializer
from user.models import SiteUser
from user.serializers import SiteUserSerializer
from userOrders.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField(read_only=True)
    products = ProductSerializer(read_only=True, many=True)
    # products_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, many=True)
    address = AddressSerializer(read_only=True)
    address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), write_only=True)
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
            "transection_id","id"
        ]

        extra_kwargs = {
            'status': {'read_only': True},
            'promocode': {'read_only': True},
            'deliveryStatus': {'read_only': True},
            'dehliveryId': {'read_only': True},
            'transection_id': {'read_only': True},
            'discount':{"read_only":True},
            'id':{"read_only":True}
        }

    def get_order_id(self, obj):
        import random
        valid = True
        orderId = "None"
        while valid == True:
            orderId = "ORDER_" + str(random.randint(1000, 1000000000))
            if Orders.objects.filter(order_id=orderId).exists():
                pass
            else:
                valid = False
        return orderId

    def create(self, validated_data):
        # products = validated_data.pop("products_id")
        obj = self.getCart(validated_data["user_id"])
        products = obj["products"]
        if  not  products:
            raise serializers.ValidationError("Cart is empty !!",code=status.HTTP_400_BAD_REQUEST)
        totalPaidAmount = obj["total"]
        address = validated_data.pop("address_id")
        user = validated_data.pop("user_id")
        if validated_data["paymentType"] == "COD":
            validated_data['status'] = "SUCCESS"
        order = Orders.objects.create(address=address, **validated_data, TotalPaidAmount=totalPaidAmount, user=user)
        for i in products:
            order.products.add(i)
        self.deleteCart(user)
        return order

    def getCart(self, obj):
        cartdata = Cart.objects.filter(user__email=obj.email)
        products = []
        amountTotal = 0
        shipping = 49
        for cart in cartdata:
            products.append(cart.product.id)
            amountTotal = amountTotal + cart.product.price
        return {"products": products, "total": amountTotal + shipping}

    def deleteCart(self, obj):
        cartdata = Cart.objects.filter(user__email=obj.email)
        cartdata.delete()

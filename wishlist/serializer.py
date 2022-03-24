from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from user.models import SiteUser
from user.serializers import SiteUserSerializer
from wishlist.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    '''Wishlist Serializer return product details in etc'''
    product_detail = serializers.SerializerMethodField()


    class Meta:
        model = Wishlist
        fields = ["product","product_detail","user"]


    def get_product_detail(self,obj):
        return ProductSerializer(instance=obj.product).data
from rest_framework import serializers

from address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    '''Address Serializer that return address details '''
    state_name = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.SerializerMethodField(read_only=True)

    def get_state_name(self,obj):
        return  obj.state.state
    def get_city_name(self,obj):
        return  obj.city.city

    class Meta:
        model = Address
        fields = ["id","user", "full_name", "phone_number", "pincode", "state", "city","city_name","state_name", "address", "address_line1", "area_colony",
                  "address_type"]




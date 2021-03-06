from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from user.models import SiteUser


class SiteUserSerializer(serializers.ModelSerializer):
    mobile_number = serializers.IntegerField(min_value=1111111111, max_value=9999999999,
                                             validators=[UniqueValidator(SiteUser.objects.all(),
                                                                         message="This mobile number is already connected with other account")],
                                             error_messages={"min_value": "Please enter valid 10 Digit Mobile Number",
                                                             "max_value": "Please enter valid 10 Digit Mobile Number"
                                                             }
                                             )
    password = serializers.CharField(write_only=True, max_length=32, min_length=8,
                                     error_messages={"max_length": "Length of password should be less then 32 Char",
                                                     "min_length": "Length of password should be grater then 8 Char"})

    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = SiteUser
        fields = ["id", "name", "email", "mobile_number", "profile_image", "password", "is_staff"]
        extra_kwargs = {"is_staff": {"read_only": True}}

    def create(self, validated_data):
        user = SiteUser(**validated_data)
        user.password = make_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "email" in validated_data:
            del validated_data["email"]
        raise_errors_on_nested_writes('update', self, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if "password" in validated_data:
            instance.password = make_password(validated_data["password"])
        instance.save()

        return instance

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            try:
                return request.build_absolute_uri(obj.profile_image.url)
            except:
                return obj.profile_image.url
        else:
            return request.build_absolute_uri("/media/media/profile_images/deafult_user_image.png")


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    default_error_messages = {
        'no_active_account': 'Please recheck Email address and Password.',
        'email_not_found': "We can not find any account assoiciated with this email address",
    }

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class CustomizedUnique(UniqueValidator):
    def filter_queryset(self, value, queryset, field_name):
        """
        Filter the queryset to all instances matching the given attribute.
        """
        filter_kwargs = {'%s__%s' % (field_name, self.lookup): value}
        return self.qs_filter(queryset, **filter_kwargs)

class SiteUserSerializerForAdmin(serializers.ModelSerializer):
    mobile_number = serializers.IntegerField(min_value=1111111111, max_value=9999999999
                                             # validators=[CustomizedUnique(SiteUser.objects.all(),
                                             #                             message="This mobile number is already connected with other account")],
                                             # error_messages={"min_value": "Please enter valid 10 Digit Mobile Number",
                                             #                 "max_value": "Please enter valid 10 Digit Mobile Number"
                                             #                 }
                                             )
    password = serializers.CharField(write_only=True, max_length=32, min_length=8,
                                     error_messages={"max_length": "Length of password should be less then 32 Char",
                                                     "min_length": "Length of password should be grater then 8 Char"})

    # profile_image = serializers.ImageField()

    class Meta:
        model = SiteUser
        fields = "__all__"
        extra_kwargs = {
            "mobile_number": {"required": False},
            "user_permissions":{"read_only": True},
            "groups": {"read_only": True}
        }
        # extra_kwargs = {"user_permissions": {"read_only": True}}

    def create(self, validated_data):
        user = SiteUser(**validated_data)
        if "mobile_number" in validated_data:
            if SiteUser.objects.filter(mobile_number__exact=validated_data["mobile_number"]).exists():
                return ValidationError("This mobile is connected to another account ")
        user.password = make_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "email" in validated_data:
            del validated_data["email"]
        raise_errors_on_nested_writes('update', self, validated_data)
        if "mobile_number" in validated_data:
            if SiteUser.objects.filter(mobile_number__exact=validated_data["mobile_number"]).exists():
                raise ValidationError({"Error":"Mobile number is connect to another account"})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if "password" in validated_data:
            instance.password = make_password(validated_data["password"])
        instance.save()

        return instance

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            try:
                return request.build_absolute_uri(obj.profile_image.url)
            except:
                return obj.profile_image.url
        else:
            return request.build_absolute_uri("/media/media/profile_images/deafult_user_image.png")

    # def __init__(self, *args, **kwargs):
    #     kwargs['partial'] = True
    #     super(SiteUserSerializerForAdmin, self).__init__(*args, **kwargs)

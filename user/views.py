from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status

from user.models import SiteUser
from user.serializers import MyTokenObtainPairSerializer, SiteUserSerializer
from rest_framework.permissions import IsAuthenticated

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SiteUserView(generics.ListCreateAPIView,generics.UpdateAPIView):

    queryset = SiteUser.objects.filter()
    serializer_class = SiteUserSerializer
    required_to_create_account = ["email","name","mobile_number","password"]

    def get_object(self):
        return SiteUser.objects.get(email=self.request.user.email)

    def get_permissions(self):
        if self.request.method == "PATCH" or self.request.method == "GET":
            self.permission_classes= [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=SiteUser.objects.get(email=self.request.user.email))
        return Response(serializer.data,status=status.HTTP_200_OK)


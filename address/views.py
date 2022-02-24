from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from address.models import Address
from address.serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated


class AdressView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class AdressActionView( generics.RetrieveUpdateDestroyAPIView ):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Address.objects.get(user__id=self.request.user.id,id=self.kwargs["id"])
        except Address.DoesNotExist:
            raise Http404


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail":"address deleted successfully "},status=status.HTTP_204_NO_CONTENT)

    
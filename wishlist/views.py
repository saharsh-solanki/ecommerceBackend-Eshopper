from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wishlist.models import Wishlist
from wishlist.serializer import WishlistSerializer

class WishlistView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


    def get_object(self):
        if "pk" in self.kwargs:
            return self.get_queryset().filter(product__id=self.kwargs["pk"])

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        if self.get_queryset().filter(product__id = request.data["product"]).exists():
            return Response({"details":"Product is already available in your wishlist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from cart.serializer import CartSerializer
from user.models import SiteUser


class CartView(generics.CreateAPIView, generics.ListAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if Cart.objects.filter(user__id=request.user.id, product__id=request.data['product']).exists():
            cart = Cart.objects.get(user__id=request.user.id, product__id=request.data['product'])
            qut = cart.quantity + 1
            if qut > 10:
                qut = qut - 1
            if "quantity" in request.data:
                qut = request.data["quantity"]
                if qut > 10:
                    return Response({"quantity": ["quantity should be less then or equal to 10"]})
            cart.quantity = qut
            cart.save()
            serializer = self.get_serializer(instance=cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            request.data["user"] = request.user.id
            if not "quantity" in request.data:
                request.data["quantity"] = 1
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        if "pk" in kwargs:
            instance = self.get_queryset().filter(product__id=kwargs["pk"])
            if instance:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"details":"Product not in your cart"},status=status.HTTP_404_NOT_FOUND)
        return Response({"product id ":["Product id is required to delete product fro cart"]},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

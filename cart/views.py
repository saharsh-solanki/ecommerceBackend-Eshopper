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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        totalProductPrice = 0
        shipping = 49
        if data:
            for cart in data:
                totalProductPrice = cart["product_detail"]["totalPrice"] + totalProductPrice
        return Response({"data":data,"totalProductPrice":totalProductPrice+shipping,"shipping":shipping,"subtotal":totalProductPrice})

    def create(self, request, *args, **kwargs):
        if Cart.objects.filter(user__id=request.user.id, product__id=request.data['product']).exists():
            cart = Cart.objects.get(user__id=request.user.id, product__id=request.data['product'])
            qut = cart.quantity
            if qut > 10:
                qut = qut - 1
            if "quantity" in request.data:
                qut = request.data["quantity"]
                if qut > 10:
                    return Response({"quantity": ["quantity should be less then or equal to 10"]})
            if "extra_info" in request.data:
                cart.extra_info = request.data["extra_info"]
            cart.quantity = qut
            cart.save()
            serializer = self.get_serializer(instance=cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            request.data["user"] = request.user.id
            if not "quantity" in request.data:
                request.data["quantity"] = 1
            request.data["product_id"] = request.data["product"]
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


class ProccedToCheckoutView( generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cartdata = serializer.data

        if not cartdata:
            return  Response({"details": "Your cart is empty"},status=status.HTTP_204_NO_CONTENT)
        for cart in cartdata:
            if cart['product']['size']:
                if "size" not in cart['extra_info']:
                    return  Response({"details": "Please select size"},status=status.HTTP_400_BAD_REQUEST)
            if cart["product"]["color"]:
                if 'color' not in cart['extra_info']:
                    return  Response({"details": "Please select color"},status=status.HTTP_400_BAD_REQUEST)
        return Response({},status=status.HTTP_200_OK)
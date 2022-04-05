from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart
from user.models import SiteUser
from userOrders.models import Orders
from userOrders.serializer import OrderSerializer, OrderSerializerForAdmin


class UserOrdersView(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(user__email=self.request.user.email)

class UserOrdersDetailView(generics.RetrieveAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(user__email=self.request.user.email)


class PaymentCODView(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Orders.objects.filter(user__email=self.request.user.email)

    def create(self, request, *args, **kwargs):
        if "paymentType" in self.request.data:
            if self.request.data["paymentType"] == "COD":
                user = SiteUser.objects.get(email=self.request.user.email)
                self.request.data["user_id"] = self.request.user.id
                serializer = self.get_serializer(data=self.request.data)
                if serializer.is_valid():
                    serializer.save()
                    return  Response(serializer.data)
                else:
                    return Response(serializer.errors)
            else:
                return  Response({"detail":"Invalid Payment Method"})




class AdminOrderView(ModelViewSet):
    ''' User View Function For Admin '''
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = OrderSerializerForAdmin
    queryset = Orders.objects.all()
    parser_classes = (MultiPartParser,)

    def update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', )
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


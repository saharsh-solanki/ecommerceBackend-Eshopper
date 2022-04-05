from django.contrib.auth.hashers import make_password
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status

from user.forms import SiteUserFrom
from user.models import SiteUser
from user.serializers import MyTokenObtainPairSerializer, SiteUserSerializer, SiteUserSerializerForAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from userOrders.models import Orders


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SiteUserView(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = SiteUser.objects.filter()
    serializer_class = SiteUserSerializer
    required_to_create_account = ["email", "name", "mobile_number", "password"]

    def get_object(self):
        return SiteUser.objects.get(email=self.request.user.email)

    def get_permissions(self):
        if self.request.method == "PATCH" or self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=SiteUser.objects.get(email=self.request.user.email))
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        if "profile_image" in request.data:
            updateUser = SiteUser.objects.get(email=user.email)
            updateUser.profile_image = request.data["profile_image"]
            updateUser.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"profile_image": "Field is required "}, status=status.HTTP_400_BAD_REQUEST)


class AdminUserView(ModelViewSet):
    ''' User View Function For Admin '''
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SiteUserSerializerForAdmin
    queryset = SiteUser.objects.all()
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


class ListAllFields(APIView):
    def get(self, request):
        import datetime
        orderQuerySet = Orders.objects.filter(order_date__month__gte=datetime.date.today().month)
        OrderedProductThisMonth = orderQuerySet.count()
        ThisMonthSale = sum(orderQuerySet.values_list("TotalPaidAmount", flat=True))
        TotalUsers = SiteUser.objects.all().count()
        return Response({"data": {"OrderedProductThisMonth": OrderedProductThisMonth, "ThisMonthSale": ThisMonthSale,
                                  "TotalUsers": TotalUsers}},status=status.HTTP_200_OK)

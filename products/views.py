import operator
from functools import reduce

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics
from rest_framework import filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Product, ProductCategory, ProductSize, ProductImage
from products.serializers import ProductSerializer, CategorySerializer, ExtraDetailSerializer, \
    ProductSerializerForAdmin, productCategrySerializerForAdmin, ProductImagesSerializerForAdmin
from django.db.models import Q


def filter_name(queryset, name, value):
    lookups = [name + '__id__in', ]
    or_queries = []
    search_terms = value.split()

    for search_term in search_terms:
        or_queries += [Q(**{lookup: search_term}) for lookup in lookups]

    return queryset.filter(reduce(operator.or_, or_queries))


class ProductFilter(django_filters.FilterSet):
    product_category = django_filters.BaseInFilter(field_name="product_category", name='product_category')

    class Meta:
        model = Product
        fields = ["product_category"]


class ProductPaggination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

class ProductView(generics.ListAPIView):
    pagination_class = ProductPaggination

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product_name", ]
    ordering_fields = ['id', "price"]

    def get_queryset(self):
        query_list = []
        if "category[]" in self.request.query_params:
            if self.request.query_params.getlist("category[]"):
                query_list.append(Q(product_category__in=self.request.query_params.getlist("category[]")))
        if "colors[]" in self.request.query_params:
            if self.request.query_params.getlist("colors[]"):
                products_ids = ProductSize.objects.filter(color__color__in= self.request.query_params.getlist("colors[]") ).values_list(
                    "product_size_key",
                    flat=True).distinct()
                query_list.append(Q(id__in=products_ids))
        if "sizes[]" in self.request.query_params:
            if self.request.query_params.getlist("sizes[]"):
                products_ids = ProductSize.objects.filter(sizes__size__in=self.request.query_params.getlist("sizes[]")).values_list(
                    "product_size_key",
                    flat=True).distinct()
                query_list.append(Q(id__in=products_ids))
        if "minPrice" in self.request.query_params and "maxPrice" in self.request.query_params:
            products_ids = ProductSize.objects.filter(
                product_size_key__price__range=(self.request.query_params.get("minPrice") , self.request.query_params.get("maxPrice"))).values_list(
                "product_size_key",
                flat=True).distinct()
            query_list.append(Q(id__in=products_ids))
        if query_list:
            return super().get_queryset().filter(reduce(operator.and_, query_list)).distinct()
        else:
            return super().get_queryset()


class SingleProductView(generics.RetrieveAPIView):

    pagination_class = ProductPaggination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductCategoryhView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer




class ExtraDetailView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ExtraDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data[0])



class AdminProductView(ModelViewSet):
    ''' User View Function For Admin '''
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = ProductSerializerForAdmin
    queryset = Product.objects.all()
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



class AdminProductCatgeoryView(ModelViewSet):
    ''' User View Function For Admin '''
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = productCategrySerializerForAdmin
    queryset = ProductCategory.objects.all()
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


class AdminProductImagesView(ModelViewSet):
    ''' User View Function For Admin '''
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = ProductImagesSerializerForAdmin
    queryset = ProductImage.objects.all()
    parser_classes = (MultiPartParser,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
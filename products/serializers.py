from django.db import connection
from django.db.migrations import serializer
from rest_framework import serializers

from products.models import Product, ProductSize, ProductCategory, ProductImage, ProductColors, Sizes


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductImagesSerializerForAdmin(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductCategorySerializer(serializers.ModelSerializer):
    '''Product Size Serialzer That return deials of product size and colors'''
    product_count = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField()

    def get_sub_category(self,obj):
        return obj.sub_category.filter().values()

    def get_product_count(self,obj):
        return Product.objects.filter(product_category__id=obj.id).count()

    class Meta:
        model = ProductCategory
        fields = ["category","icon","id","sub_category","product_count"]


class ProductSerializerForAdmin(serializers.ModelSerializer):
    '''Product Serializer return product details related to other modals also'''
    category  = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        # fields = ["product_name", "id", "price", "description", "size", "color", "stock_detail","images"]
        fields = "__all__"


    def get_category(self,obj):
        return  list(ProductCategory.objects.all().values("id","category","icon"))


class ProductSizeSerializer(serializers.ModelSerializer):
    '''Product Size Serialzer That return deials of product size and colors'''
    sizes = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    def get_sizes(self, obj):
        return obj.sizes.size

    def get_color(self, obj):
        return obj.color.color

    class Meta:
        model = ProductSize
        fields = ["sizes", "stock", "color", "productOrderCount"]


class ProductSerializer(serializers.ModelSerializer):
    '''Product Serializer return product details related to other modals also'''
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    stock_detail = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def count(self):
        return self.instance.count()

    def get_size(self, obj):
        # return ProductSize.objects.filter(product_size_key__id=obj.id).values_list("sizes__size", flat=True)
        return list(ProductSize.objects.filter(product_size_key__id=obj.id).values_list("sizes__size",flat=True).distinct())

    def get_color(self, obj):
        # return ProductSize.objects.filter(product_size_key__id=obj.id).values_list("color__color", flat=True)
        return list(ProductSize.objects.filter(product_size_key__id=obj.id).values_list("color__color",flat=True).distinct())

    def get_stock_detail(self, obj):
        stock_obj = ProductSize.objects.filter(product_size_key__id=obj.id)
        return {"total_stock": sum(stock_obj.values_list("stock", flat=True)),
                "total_ordered_product": sum(stock_obj.values_list("productOrderCount", flat=True)),
                "in_stock": True if sum(stock_obj.values_list("stock", flat=True)) >= sum(
                    stock_obj.values_list("productOrderCount", flat=True)) else False}

    def get_images(self, obj):
        image = ProductImageSerializer(instance=ProductImage.objects.filter(product_image_key__id=obj.id).first())
        images = ProductImageSerializer(instance= ProductImage.objects.filter(product_image_key__id=obj.id) , many=True )
        return {"image": image.data,
                "images": images.data,
              }

    class Meta:
        model = Product
        fields = ["product_name", "id", "price", "description", "size", "color", "stock_detail","images"]


class CategorySerializer(serializers.ModelSerializer):
    '''Product Category Serializer Return the name of category and sub category'''
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ["category", "sub_category","icon"]

    def get_sub_category(self, obj):
        return obj.sub_category.all().values_list("category", flat=True)

class productCategrySerializerForAdmin(serializers.ModelSerializer):
    '''Product Category Serializer Return the name of category and sub category'''
    # sub_category = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = "__all__"# ["category", "sub_category","icon"]

    # def get_sub_category(self, obj):
    #     return obj.sub_category.all().values_list("category", flat=True)



class ExtraDetailSerializer(serializers.Serializer):
    slider_product = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()
    trandy_product = serializers.SerializerMethodField()
    latest_product = serializers.SerializerMethodField()
    colors_for_fillter = serializers.SerializerMethodField()
    sizes_for_fillter = serializers.SerializerMethodField()

    def get_colors_for_fillter(self,obj):
        return ProductColors.objects.all().distinct().values_list("color",flat=True)

    def get_sizes_for_fillter(self,obj):
        return Sizes.objects.all().distinct().values_list("size",flat=True)

    def get_slider_product(self, obj):
        return ProductImage.objects.all().order_by("?")[:5].values("product_image_key__product_name","image")

    def get_top_category(self, obj):
        return ProductCategorySerializer(ProductCategory.objects.filter().order_by("?")[:6],many=True).data

    def get_trandy_product(self, obj):
        return ProductSerializer(Product.objects.all().order_by("?")[:5],many=True).data

    def get_latest_product(self, obj):
        return ProductSerializer(Product.objects.all().order_by("-id")[:5],many=True).data


    class Meta:
        fields = ["slider_product","top_category","trandy_product","latest_product","colors_for_fillter","sizes_for_fillter"]

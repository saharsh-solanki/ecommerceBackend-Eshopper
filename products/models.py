from django.db import models

# Create your models here.
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Product(models.Model):
    '''Product Model'''
    product_name = models.CharField(max_length=250)
    price = models.FloatField(max_length=100)
    description = models.TextField(max_length=400, blank=True, null=True,
                                   default="Description is not available for this product")
    product_category = models.ManyToManyField("ProductCategory", related_name="product_category", null=True, blank=True)
    color_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.product_name

    # instance.save()


class Sizes(models.Model):
    ''' Size Model We Multiple Size '''
    size = models.CharField(max_length=250)

    def __str__(self):
        return self.size


class ProductColors(models.Model):
    ''' Colors For product '''
    color = models.CharField(max_length=250)

    def __str__(self):
        return self.color


class ProductSize(models.Model):
    '''
    Prodcut size model stock in interger field that hold the current product stock
    productOrderCount is number of product that are ordered
    '''
    product_size_key = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_size_key")
    sizes = models.ForeignKey(Sizes, related_name="SizesOfProduct", on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    color = models.ForeignKey(ProductColors, related_name="ColorOfProduct", on_delete=models.CASCADE, null=True,
                              blank=True)
    productOrderCount = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.product_size_key.product_name
    #
    # def save(self, *args, **kwargs):
    #     self.color_json = ProductColors.objects.filter(id=self.color.id).values().first()
    #     super(ProductSize, self).save()


# @receiver(post_save,sender=ProductSize)
# def save_color_copy_in_otherField(sender,instance,**kwargs):
#     instance.update(color_json={"ID":1212})
#     # instance.save()


class ProductImage(models.Model):
    '''Product model for Multiple Images '''
    product_image_key = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image_key")
    image = models.ImageField(upload_to='ProductImages')

    def __str__(self):
        return self.product_image_key.product_name


class ProductCategory(models.Model):
    icon = models.ImageField(upload_to='media/category_icon', null=True, blank=True)
    category = models.CharField(max_length=250)
    sub_category = models.ManyToManyField("ProductCategory", related_name="product_sub_category", null=True, blank=True)

    def __str__(self):
        return self.category


# @receiver(post_save, sender=Product)
# def save_color_copy_in_otherField(sender, instance, created, **kwargs):
#     if not created:
#         # instance.color_json = {"ID": 1212}
#         # instance.save()
#         prod = Product.objects.filter(id=instance.id)
#         prod.update(color_json=
#                     list(ProductSize.objects.filter
#                     (product_size_key__id=prod.first().id).values("sizes__size", "product_size_key_id", "stock",
#                                                                   "color__color", "productOrderCount"))
#                     )

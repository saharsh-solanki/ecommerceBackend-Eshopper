from django.db import models


# Create your models here.
class Product(models.Model):
    '''Product Model'''
    product_name = models.CharField(max_length=250)
    price = models.FloatField(max_length=100)
    description = models.TextField(max_length=400,blank=True,null=True,default="Description is not available for this product")
    product_category = models.ManyToManyField("ProductCategory",related_name="product_category",null=True,blank=True)

    def __str__(self):
        return  self.product_name


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
    sizes = models.ForeignKey(Sizes, related_name="SizesOfProduct",on_delete=models.CASCADE)
    stock = models.IntegerField( null=True, blank=True)
    color = models.ForeignKey(ProductColors, related_name="ColorOfProduct",on_delete=models.CASCADE,null=True,blank=True)
    productOrderCount = models.IntegerField( null=True,default=0)


    def __str__(self):
        return  self.product_size_key.product_name



class ProductImage(models.Model):
    '''Product model for Multiple Images '''
    product_image_key = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image_key")
    image = models.ImageField(upload_to='ProductImages')

    def __str__(self):
        return  self.product_image_key.product_name



class ProductCategory(models.Model):
    category = models.CharField(max_length=250)
    sub_category = models.ManyToManyField("ProductCategory",related_name="product_sub_category",null=True,blank=True)

    def __str__(self):
        return self.category
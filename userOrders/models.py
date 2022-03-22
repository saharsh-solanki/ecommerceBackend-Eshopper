from django.db import models

# Create your models here.
from address.models import Address
from products.models import Product
from user.models import SiteUser


class Orders(models.Model):
    '''Orders model contains order of user '''

    StatusChoices = [
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED")
    ]
    paymentTypeChoices = [
        ("COD", "Cash on delivery"),
        ("ONLINE", "online")
    ]
    dehliveryStatusChoices = [
        ("PROCESSING", "We Are Processing Your Order"),
        ("SHIPPED", "You order is Shipped"),
        ("PACKED", "your order is packed"),
        ("OUTFROMWAREHOUSE", "Your Order is taken by dehlivery services")
    ]

    order_id = models.CharField(max_length=100)
    user = models.ForeignKey(SiteUser,related_name="OrderUser",on_delete=models.CASCADE)
    products = models.JSONField(default=dict)
    cartdata = models.JSONField(default=dict)
    address = models.JSONField(default=dict)
    order_date = models.DateTimeField(auto_now=True)
    TotalPaidAmount  = models.FloatField()
    status = models.CharField(max_length=100,choices=StatusChoices,default="PENDING")
    paymentType = models.CharField(max_length=100,choices=paymentTypeChoices)
    discount = models.FloatField(max_length=100,default=0)
    promocode = models.CharField(max_length=100, null=True,blank=True)
    deliveryStatus = models.CharField(max_length=100,choices=dehliveryStatusChoices,default="PROCESSING")
    dehliveryId = models.CharField(max_length=100,null=True,blank=True)
    transection_id = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.user.email

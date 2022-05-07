from django.db import models

# Create your models here.
from products.models import Product
from user.models import SiteUser


class Cart(models.Model):
    user = models.ForeignKey(SiteUser,related_name="CartUser",on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="CartProduct",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    extra_info = models.JSONField(default=dict)
from django.db import models

# Create your models here.
from products.models import Product
from user.models import SiteUser


class Wishlist(models.Model):
    user = models.ForeignKey(SiteUser,related_name="WishlistUser",on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="WishlistProduct",on_delete=models.CASCADE)
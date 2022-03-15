from django.contrib import admin

# Register your models here.
from userOrders.models import Orders

admin.site.register(Orders)
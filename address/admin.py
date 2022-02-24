from django.contrib import admin

# Register your models here.
from address.models import Address, City, State

admin.site.register(Address)
admin.site.register(City)
admin.site.register(State)
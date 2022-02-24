from django.contrib import admin

# Register your models here.
from user.models import SiteUser

admin.site.register(SiteUser)
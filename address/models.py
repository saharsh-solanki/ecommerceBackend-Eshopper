from django.db import models

# Create your models here.
from user.models import SiteUser


class State(models.Model):
    ''' State Model for address contains list of address '''
    state  = models.CharField(max_length=40)

    def __str__(self):
        return self.state


class City(models.Model):
    ''' City model contains list of cities associated with state '''
    city  = models.CharField(max_length=40)

    def __str__(self):
        return self.city


class StateAndCity(models.Model):
    ''' Model tell us which city belong to which state '''
    rel_state = models.ForeignKey(State,related_name="related_state",on_delete=models.CASCADE)
    rel_city_to = models.ManyToManyField(City,related_name="rel_city_to")

    def __str__(self):
        return self.rel_state.state



class Address(models.Model):
    ''' Contains address of user '''
    user = models.ForeignKey(SiteUser,related_name="AddressUser",on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    pincode = models.IntegerField()
    state = models.ForeignKey(State, related_name="address_state", on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name="address_city", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100,null=True,blank=True)
    area_colony = models.CharField(max_length=100, null=True, blank=True)
    address_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.email




from django.db import models
from django.contrib.auth.models import User
from datetime import  date
from account.models import *


class Customer(models.Model):
    customer_name = models.CharField(max_length=255,null=True)
    phone_no = models.CharField(max_length=10, null=True)
    gstin_no = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    address1 = models.TextField()
    city1 = models.ForeignKey(City, on_delete=models.CASCADE,related_name="city1",null=True)
    state1 = models.ForeignKey(State, on_delete=models.CASCADE,related_name="state1",null=True)
    country1 = models.ForeignKey(Country, on_delete=models.CASCADE,related_name="country1",null=True)
    pincode1 = models.CharField(max_length=6)
    contact_person1 = models.CharField(max_length=255,null=True,blank=True)
    mobile_no1 = models.CharField(max_length=10,null=True,blank=True)
    contact_person_email1 = models.EmailField(null=True,blank=True)
    place_of_testing = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    city2 = models.ForeignKey(City, on_delete=models.CASCADE,related_name="city2",blank=True,null=True)
    state2 = models.ForeignKey(State, on_delete=models.CASCADE,related_name="state2",blank=True,null=True)
    country2 = models.ForeignKey(Country, on_delete=models.CASCADE,related_name="country2",blank=True,null=True)
    pincode2 = models.CharField(max_length=10, null=True, blank=True)
    contact_person2 = models.CharField(max_length=255, null=True, blank=True)
    mobile_no2 = models.CharField(max_length=10, null=True, blank=True)
    contact_person_email2 = models.EmailField(null=True, blank=True)
    is_quatation_customer  = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cus_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cus_modified_by")
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.customer_name:
            return self.customer_name
        else:
            return "Empty"
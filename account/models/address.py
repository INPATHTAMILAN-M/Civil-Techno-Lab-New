from django.db import models
from django.contrib.auth.models import User
from datetime import  date


class State(models.Model):
    name = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="city_created_by",null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.name
from django.db import models
from django.contrib.auth.models import User
from datetime import  date

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=255)
    address = models.TextField()
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=1, choices= [('M','Male'),
                                                      ('F','Female')])
    qualification = models.CharField(max_length=255)
    joining_date = models.DateTimeField()
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="emp_created_by",null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="emp_modified_by",null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)
    branch_email =  models.EmailField(null=True)
    signature = models.ImageField(null=True,blank=True,upload_to="signature")
    role = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.employee_name




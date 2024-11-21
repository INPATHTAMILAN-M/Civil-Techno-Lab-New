from django.db import models
from django.contrib.auth.models import User
from datetime import  date

gender_choices = [('M','Male'),('F','Female'),]

'''
class Common(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="modified_by")
    modified_date = models.DateTimeField(auto_now=True)

'''

class City(models.Model):
    name = models.CharField(max_length=255,null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="city_created_by",null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.name
    
class State(models.Model):
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True)
    phone_no = models.CharField(max_length=10)
    gstin_no = models.CharField(max_length=15)
    email = models.EmailField()
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

    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cus_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cus_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    #def __str__(self):
        #return self.user.username

    def __str__(self):
        if self.customer_name:
            return self.customer_name
        else:
            return "Empty"

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=255)
    address = models.TextField()
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField(null=True,blank=True)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=1, choices= gender_choices)
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
    
    def __str__(self):
        return self.employee_name



class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,  # Allow null values when the user is deleted
        blank=True
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    login_at = models.DateTimeField(auto_now_add=True)  # Automatically log the timestamp
    details = models.TextField(blank=True, null=True)  # Additional details about the action
    login_ip = models.GenericIPAddressField(blank=True, null=True)  # IP address of the user

    def __str__(self):
        return super().__str__()
       
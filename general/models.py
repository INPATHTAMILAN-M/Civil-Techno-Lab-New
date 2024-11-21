from django.db import models
from django.contrib.auth.models import User
from datetime import  date
from ckeditor_uploader.fields import RichTextUploadingField

tax_status_choices= [('E','Enable'),('D','Disable'),]

class Tax(models.Model):
    tax_name = models.CharField(max_length=255)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_status = models.CharField(max_length=1, choices=tax_status_choices, default='E')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tax_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tax_name


class Print_Format(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="print_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Letter_Pad_Logo(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Material(models.Model):
    material_name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="material_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)

    template = models.TextField(null=True)
    print_format = models.ForeignKey(Print_Format, on_delete=models.CASCADE,null=True)
    letter_pad_logo = models.ForeignKey(Letter_Pad_Logo, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.material_name
    


class Report_Template(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    report_template_name = models.CharField(max_length=255)
    template = models.TextField(null=True)
    print_format = models.ForeignKey(Print_Format, on_delete=models.CASCADE)
    letter_pad_logo = models.ForeignKey(Letter_Pad_Logo, on_delete=models.CASCADE)

    def __str__(self):
        return self.report_template_name

class Test(models.Model):
    material_name = models.ForeignKey(Material, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="test_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.test_name

class Expense(models.Model):
    expense_name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="expense_created_by")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="expense_modified_by")
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.expense_name


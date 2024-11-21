from django.db import models
from account.models import Customer
from django.contrib.auth.models import User
from general.models import Material,Expense,Test,Report_Template,Tax
from django.db.models import Sum
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import Employee
import os
from uuid import uuid4

tax_choices = [('cgst_sgst','CGST & SGST'),('igst','IGST'),]
payment_mode_choices = [('cash','Cash'),('cheque','Cheque'),('upi','UPI'),('neft','NEFT'),('tds','TDS')]
invoice_test_choices = [('Yes','Yes'),('No','No'),]
#expense_category_choices = [('salary', 'Salary'),('office_expense', 'Office Expense'),('office_sub_work', 'Office Sub Work'),('tds', 'TDS'),('gst', 'GST'),('rent', 'Rent'),]

class SalesMode(models.Model):
    sales_mode = models.CharField(max_length=55)
    def __str__(self):
        return self.sales_mode

class Invoice(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_mode = models.ForeignKey(SalesMode, on_delete=models.CASCADE,null=True,blank=True)
    project_name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax = models.ManyToManyField(Tax,null=True,blank=True)
    advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tds_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    fully_paid = models.BooleanField(default=False)
    date  = models.DateField(null=True)
    invoice_no = models.CharField(null=True,max_length=20)

    payment_mode = models.CharField(max_length=6, choices= payment_mode_choices,null=True)
    cheque_number = models.CharField(max_length=50, null=True, blank=True)
    upi = models.CharField(max_length=150, null=True, blank=True)
    bank = models.CharField(max_length=255, null=True, blank=True)
    amount_paid_date = models.DateField(null=True,blank=True)

    invoice_image = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="invoice_created_by",null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)
    place_of_testing = models.CharField(max_length=255, null=True, blank=True)
    completed = models.CharField(max_length=6, choices= invoice_test_choices,default="No")


    '''material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rate_per_sample = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    amount_before_tax = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    amount_after_tax = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    tax_option = models.CharField(max_length=10, choices=tax_choices)'''

    @property
    def incompleted_test(self):
        count  = Invoice_Test.objects.filter(invoice=self,completed="No").count()
        return count
    


    @property
    def customer_name(self):
        return str(self.customer.customer_name)
    
    @property
    def customer_gst_no(self):
        return str(self.customer.gstin_no)
    
    @property
    def amount(self):
        total = Invoice_Test.objects.filter(invoice=self).aggregate(Sum('total')) 
        try:
            return total['total__sum']
        except:
            return 0
    
    @property
    def cgst_tax(self):
        taxes = self.tax.all()
        for tax in taxes:
            if "CGST" == str(tax):
                tax_percentage = tax.tax_percentage      
                try:
                    return round((self.get_after_discount * tax.tax_percentage )/100,2)
                except:
                    return 0
        else:
            return 0

        
    @property
    def igst_tax(self):
        taxes = self.tax.all()
        for tax in taxes:
            if "IGST" == str(tax):
                tax_percentage = tax.tax_percentage                 
                return round((self.get_after_discount * tax.tax_percentage )/100,2)
            
        else:
            return 0
            

        

    
    @property
    def get_after_discount(self):
        try:
            return self.amount - (self.amount * self.discount)/100
        except:
            return 0

    

    
    
    @property
    def sgst_tax(self):
        taxes = self.tax.all()
        for tax in taxes:
            if "SGST" == str(tax):
                tax_percentage = tax.tax_percentage                 
                return round((self.get_after_discount * tax.tax_percentage )/100,2)
            
        else:
            return 0

        

    @property
    def cheque_neft(self):
        return self.cheque_number
    
    @property
    def tax_deduction(self):
        return 0
    

    @property
    def cash(self):
        return 0
    

    @property
    def incompleted_test(self):
        count  = Invoice_Test.objects.filter(invoice=self,completed="No").count()
        return count
    


class Invoice_Test(models.Model):    
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True,blank=True)
    customer =  models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    price_per_sample  = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    report_template = models.TextField(null=True,blank=True)
    invoice_image = models.CharField(max_length=255, null=True, blank=True)
    completed = models.CharField(max_length=6, choices= invoice_test_choices,default="No")
    signature = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    is_authorised_signatory = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="invoice_test_created_by",null=True)
    created_date = models.DateField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)
    ulr = models.CharField(max_length=255, null=True, blank=True)


    @property
    def count(self):
        records   = Invoice_Test.objects.filter(invoice=self.invoice,id__lt=self.id).count()
        if records == 0:
            position = 1
        else:
            position = records +1
        
        return position
    
    @property
    def customer(self):
        return str(self.invoice.customer)
    
    @classmethod
    @property
    def next_ulr(cls):
        # Filter the last record based on specific criteria
        last_object = cls.objects.filter(test__material_name__material_name="Rebound Hammer").last()
        
        # Check if last_object exists and has a ULR
        if last_object and last_object.ulr:
            # Extract numeric part and increment it
            prefix = last_object.ulr[:10]  # "TC14811240"
            numeric_part = int(last_object.ulr[10:18])  # Extract "00000002"
            new_numeric_part = f"{numeric_part + 1:08d}"  # Increment and format as 8 digits
            suffix = last_object.ulr[18:]  # "F"
            
            # Combine parts to create new ULR
            return f"{prefix}{new_numeric_part}{suffix}"
        else:
            # Return the initial format if no last_object exists
            return "TC1481124000000001F"
    
    @property
    def invoice_no(self):
        try:
            return str(self.invoice.invoice_no)
        except:
            pass

    def save(self, *args, **kwargs):
        # Only set the ULR if it is not already set
        if not self.ulr:
            self.ulr = self.__class__.next_ulr  # Access next_ulr through the class
        super().save(*args, **kwargs)  


class Test_Report(models.Model):
    invoice_test = models.ForeignKey(Invoice_Test,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    report_template = models.ForeignKey(Report_Template,on_delete=models.CASCADE)


class Receipt(models.Model):
    invoice_no = models.ForeignKey(Invoice,on_delete=models.CASCADE,null=True)
    payment_mode = models.CharField(max_length=6, choices= payment_mode_choices)
    cheque_number = models.CharField(max_length=50, null=True, blank=True)
    upi = models.CharField(max_length=150, null=True, blank=True)
    neft = models.CharField(max_length=150, null=True, blank=True)
    tds = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    
    amount  = models.DecimalField(max_digits=20, decimal_places=2, default=0)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="payment_added_by",null=True)
    created_date = models.DateField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)


    #def __str__(self):
        #return self.customer_name

'''class Expense_user(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name'''

class Expense_Entry(models.Model):
    date = models.DateTimeField()
    expense_user =  models.CharField(max_length=250)
    expense_category = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="entry_created_by",null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)
    

class Invoice_File_Category(models.Model):
    name =  models.CharField(max_length=250)


    def __str__(self):
        return self.name
   

def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # get filename

    if instance.invoice:
        filename =  str(instance.invoice.invoice_no)+"_invoice"+str(uuid4().hex)+"."+str(ext)
        
    elif instance.expense:      
        filename = str(instance.expense.id)+"_expense"+str(uuid4().hex)+"."+str(ext)
    
    # return the whole path to the file
    return os.path.join('invoice_files/', filename)



class Invoice_File(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,null=True,blank=True)
    expense = models.ForeignKey(Expense_Entry, on_delete=models.CASCADE,null=True,blank=True)

    file = models.FileField(upload_to=wrapper)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="invoice_file_created_by",null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    modified_date = models.DateTimeField(auto_now=True,null=True)
    category = models.ForeignKey(Invoice_File_Category, on_delete=models.CASCADE,null=True)


    @property
    def expense_user(self):
        return self.expense.expense_user
    
    @property
    def expense_amount(self):
        return self.expense.amount
    

    @property
    def expense_date(self):        
        return self.expense.date
    

    @property
    def invoice_no(self):        
        return self.invoice.invoice_no
    

    @property
    def invoice_customer(self):        
        return str(self.invoice.customer)
    
    @property
    def invoice_amount(self):
        return str(self.invoice.total_amount)
    
    @property
    def invoice_date(self):
        return str(self.invoice.date)



    





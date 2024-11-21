from rest_framework import serializers
from .models import Expense_Entry,Invoice,SalesMode,Invoice_Test, Invoice_File, Invoice_File_Category, Receipt
from general.models import Material,Expense,Test,Tax
from account.models import Customer
from num2words import num2words
from bs4 import BeautifulSoup


class Receipt_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['invoice_no','payment_mode','cheque_number','upi','date','amount','neft','tds']

class Receipt_Serializer_List(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id','invoice_no','payment_mode','cheque_number','upi','date','amount','neft','tds']


class Invoice_File_Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_File_Category
        fields = '__all__'

class Create_Expense_Entry_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Expense_Entry
        fields = ['id','date','expense_user','expense_category','amount','narration']

class Expense_Entry_Serializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    modified_by = serializers.StringRelatedField()
    expense_category_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense_Entry
        fields = ['id','expense_user','date','amount','expense_category','narration','created_by','created_date','modified_by','modified_date','expense_category_name']

    def get_expense_category_name(self,obj):
        return str(obj.expense_category)
    
class Expense_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'expense_name']



class Customer_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','customer_name','address1','phone_no']

class Sales_mode_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = SalesMode
        fields = ['id','sales_mode'] 

class Tax_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id','tax_name','tax_percentage']

class Create_Invoice_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','customer','sales_mode','project_name','discount','tax','advance','balance']

class Edit_Invoice_Serializer(serializers.ModelSerializer):
    #date = serializers.DateField(input_formats=['%d-%m-%Y',])

    class Meta:
        model = Invoice
        fields = ['id','customer','sales_mode','project_name','discount','tax','total_amount','tds_amount','advance','balance','amount_paid_date','bank','cheque_number','payment_mode','date','place_of_testing','upi','completed']

class Invoice_Serializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    incompleted_test = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ['id','invoice_no','date','customer','sales_mode','project_name','discount','tax','advance','balance','place_of_testing','total_amount','incompleted_test']

    def get_incompleted_test(self,obj):
        return str(obj.incompleted_test)
    
class Material_Serializer2(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']

class Material_Test_Serializer(serializers.ModelSerializer):  
    test_material_id = serializers.SerializerMethodField()
    test_material_name = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'test_name', 'test_material_id','test_material_name', 'price_per_piece']

    def get_test_material_id(self, obj):
        return str(obj.material_name.id)

    def get_test_material_name(self, obj):
        return str(obj.material_name.material_name)

class Create_Invoice_Test_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice_Test
        fields = ['invoice','test','quantity','price_per_sample','total']

import re

class Invoice_Test_Serializer(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    final_html = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    without_header_footer = serializers.SerializerMethodField()

    class Meta:
        model = Invoice_Test
        fields = ['id','invoice','test','test_name','quantity','price_per_sample','total','report_template','final_html','count','completed','signature','invoice_image','without_header_footer','is_authorised_signatory']   

    def get_test_name(self,obj):
        return obj.test.test_name
    
    def get_count(self,obj):
        return str(obj.count)
    
    def get_without_header_footer(self,obj):

        if obj.signature:
           
            data  = obj.report_template
            soup = BeautifulSoup(data, 'html.parser')
            # Find and remove the image tag with the specific src
            img_tag = soup.find('img', {'src': 'https://files.covaiciviltechlab.com/static/header-hammer.png'})
            if img_tag:
                img_tag.extract()

            # Convert back to string after modification
            data = str(soup)
            data = data.replace('<img src="https://files.covaiciviltechlab.com/static/header.gif" alt="Logo">','')  
            data = data.replace('<img alt="Logo" src="https://files.covaiciviltechlab.com/static/header.gif"/>','')                        
            data = data.replace('<tr>','',1)
            data = data.replace('<td colspan="2">','',1)
            data = data.replace('</td>','',1)
            data = data.replace('</tr>','',1)
            data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:none !important;"><p><img src="https://files.covaiciviltechlab.com/static/ragu r.png"  height="150px" width="150px"></p><p style="text-align:justify"><strong>M.RAGURAM, ME (STRUCTURAL)., AMIE <br>CHARTERED ENGINEER (AM 1818123)<br>Covai Civil Lab Private Limited </strong></p></td><td width="40%"  style="border:0 !important;"><p id="dynamic-signature"><img src="https://files.covaiciviltechlab.com/media/'+str(obj.signature.signature)+'" height="150px" width="150px"></p><p style="font-size:12px"><strong style="font-size:12px">'+str(obj.signature)+'<br>'+str(obj.signature.role)+'</strong></p><p style="font-size:12px"><strong>Covai Civil Lab Private Limited</strong></p>  </td> <td width="20%"  style="border:0 !important;" class="qr-code"> <img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'" ></td> </tr></table></figure>'
            #data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:none !important;"><p><img src="https://files.covaiciviltechlab.com/static/ragu r.png"  height="150px" width="150px"></p><p style="font-size:12px"><strong  style="font-size:12px">M.RAGURAM, ME (STRUCTURAL)., AMIE <br>CHARTERED ENGINEER (AM 1818123)<br>Covai Civil Lab Private Limited </strong></p></td><td width="40%"  style="border:0 !important;"><p id="dynamic-signature"><img src="https://files.covaiciviltechlab.com/media/'+str(obj.signature.signature)+'" height="150px" width="150px"></p><p style="font-size:12px"><strong style="font-size:12px">'+str(obj.signature)+'<br>'+str(obj.signature.role)+'</strong></p><p style="font-size:12px"><strong>Covai Civil Lab Private Limited</strong></p> </td> <td width="20%"  style="border:0 !important;" class="qr-code"> <img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'" ></td> </tr> <tr><td colspan="3" style="border:0 !important;"> <hr style="color: #000;"></td></tr> <tr style="border-spacing:0.6pt; border:0 !important;"> <td colspan="3" style="border:0px !important; border-style:inset; border-width:0.75pt; vertical-align:middle"> <p><img alt="Logo" src="https://files.covaiciviltechlab.com/static/test-footer.png" style="width:100%" /></p> </td> </tr> </table></figure>'
            soup = BeautifulSoup(data, 'html.parser')
            first_table = str(soup.select_one("table:nth-of-type(1)"))    
            #data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:none !important;"><p><img src="https://files.covaiciviltechlab.com/static/ragu r.png"  height="150px" width="150px"></p><p style="text-align:justify"><strong>M.RAGURAM, ME (STRUCTURAL)., AMIE <br>CHARTERED ENGINEER (AM 1818123)<br>Covai Civil Lab Private Limited </strong></p></td><td width="40%"  style="border:0 !important;"><p id="dynamic-signature"><br><br></p><p style="text-align:justify"><strong>'+str(obj.signature)+'<br>'+str(obj.signature.role)+'</strong></p><p style="text-align:justify"><strong>Covai Civil Lab Private Limited</strong></p> </td> <td width="20%"  style="border:0 !important;" class="qr-code"> <img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'" ></td> </tr> <tr><td colspan="3" style="border:0 !important;"> <hr style="color: #000;"></td></tr> <tr style="border-spacing:0.6pt; border:0 !important;">  </tr> </table></figure>'
            text_to_replace = "Page Break"
            # Replace text
            count = 1
     
           
            
            text_occurrences = soup.find_all('p', text=re.compile('Page Break'))
            for element in text_occurrences:  
                count = count +1                
                first_table_updated = first_table.replace('Page No: 1','Page No: '+str(count)) 
                first_table_updated = first_table.replace('Page No:1','Page No: '+str(count)) 
                first_table_updated = first_table.replace('Page No:   1','Page No: '+str(count)) 
                first_table_updated = first_table_updated.replace('<table','<table style="margin-bottom:10px !important" class="pagebreak"')        
                new_content = BeautifulSoup(first_table_updated, 'html.parser') 
                tr_elements = new_content.find_all('tr')

                # Check if there are at least three <tr> elements
                if len(tr_elements) >= 3:
                    # Remove the third <tr> element
                    tr_elements[2].decompose()            
                element.replace_with(new_content)
                    
            soup.prettify()
            data  = str(soup)
            #data = data.replace('Page Break','<div class="pagebreak"> </div>')
            return data
        
        elif obj.is_authorised_signatory:

            data  = obj.report_template
            soup = BeautifulSoup(data, 'html.parser')
            # Find and remove the image tag with the specific src
            img_tag = soup.find('img', {'src': 'https://files.covaiciviltechlab.com/static/header-hammer.png'})
            if img_tag:
                img_tag.extract()

            # Convert back to string after modification
            data = str(soup)
            data = data.replace('<img src="https://files.covaiciviltechlab.com/static/header.gif" alt="Logo">','')  
            data = data.replace('<img alt="Logo" src="https://files.covaiciviltechlab.com/static/header.gif"/>','')                        
            data = data.replace('<tr>','',1)
            data = data.replace('<td colspan="2">','',1)
            data = data.replace('</td>','',1)
            data = data.replace('</tr>','',1)
            data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:0 !important;"><p id="dynamic-signature"></p><p style="font-size:12px"><strong style="font-size:12px"><br><br>Authorised Signatory</strong></p><p style="font-size:12px"><strong>Covai Civil Lab Private Limited</strong></p></td><td width="40%" style="border:none !important;"><p></p><p style="text-align:justify"></p></td><td width="20%" style="border:0 !important;" class="qr-code"><img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'"></td></tr><tr><td colspan="3" style="border:0 !important;"><hr style="color: #000;"></td></tr><tr style="border-spacing:0.6pt; border:0 !important;"><td colspan="3" style="border:0px !important; border-style:inset; border-width:0.75pt; vertical-align:middle"></td></tr></table></figure>'
            soup = BeautifulSoup(data, 'html.parser')
            first_table = str(soup.select_one("table:nth-of-type(1)"))    
     

            #data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:none !important;"><p><img src="https://files.covaiciviltechlab.com/static/ragu r.png"  height="150px" width="150px"></p><p style="text-align:justify"><strong>M.RAGURAM, ME (STRUCTURAL)., AMIE <br>CHARTERED ENGINEER (AM 1818123)<br>Covai Civil Lab Private Limited </strong></p></td><td width="40%"  style="border:0 !important;"><p id="dynamic-signature"><br><br></p><p style="text-align:justify"><strong>'+str(obj.signature)+'<br>'+str(obj.signature.role)+'</strong></p><p style="text-align:justify"><strong>Covai Civil Lab Private Limited</strong></p> </td> <td width="20%"  style="border:0 !important;" class="qr-code"> <img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'" ></td> </tr> <tr><td colspan="3" style="border:0 !important;"> <hr style="color: #000;"></td></tr> <tr style="border-spacing:0.6pt; border:0 !important;">  </tr> </table></figure>'
            
            text_to_replace = "Page Break"

            # Replace text
            count = 1           
            
            text_occurrences = soup.find_all('p', text=re.compile('Page Break'))
            for element in text_occurrences:  
                count = count +1                
                first_table_updated = first_table.replace('Page No: 1','Page No: '+str(count)) 
                first_table_updated = first_table.replace('Page No:1','Page No: '+str(count)) 
                first_table_updated = first_table.replace('Page No:   1','Page No: '+str(count)) 
                first_table_updated = first_table_updated.replace('<table','<table style="margin-bottom:10px !important" class="pagebreak"')        
                new_content = BeautifulSoup(first_table_updated, 'html.parser') 
                tr_elements = new_content.find_all('tr')

                # Check if there are at least three <tr> elements
                if len(tr_elements) >= 3:
                    # Remove the third <tr> element
                    tr_elements[2].decompose()            
                element.replace_with(new_content)
                
                
            soup.prettify()
            data  = str(soup)
            #data = data.replace('Page Break','<div class="pagebreak"> </div>')
            return data

        else:
            return None

    
    
    def get_final_html(self,obj):

        if obj.signature:
            data = obj.report_template
            data = data.replace('Page Break','<div class="pagebreak"> </div>')
            data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:none !important;"><p><img src="https://files.covaiciviltechlab.com/static/ragu r.png"  height="150px" width="150px"></p><p style="font-size:12px"><strong  style="font-size:12px">M.RAGURAM, ME (STRUCTURAL)., AMIE <br>CHARTERED ENGINEER (AM 1818123)<br>Covai Civil Lab Private Limited </strong></p></td><td width="40%"  style="border:0 !important;"><p id="dynamic-signature"><img src="https://files.covaiciviltechlab.com/media/'+str(obj.signature.signature)+'" height="150px" width="150px"></p><p style="font-size:12px"><strong style="font-size:12px">'+str(obj.signature)+'<br>'+str(obj.signature.role)+'</strong></p><p style="font-size:12px"><strong>Covai Civil Lab Private Limited</strong></p> </td> <td width="20%"  style="border:0 !important;" class="qr-code"> <img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'" ></td> </tr> <tr><td colspan="3" style="border:0 !important;"> <hr style="color: #000;"></td></tr> <tr style="border-spacing:0.6pt; border:0 !important;"> <td colspan="3" style="border:0px !important; border-style:inset; border-width:0.75pt; vertical-align:middle"> <p><img alt="Logo" src="https://files.covaiciviltechlab.com/static/test-footer.png" style="width:100%" /></p> </td> </tr> </table></figure>'
            return data
        elif obj.is_authorised_signatory:
            data = obj.report_template
            data = data.replace('Page Break','<div class="pagebreak"> </div>')
            data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:none !important; border-spacing:0.6pt; width:100%"><tr><td width="40%" style="border:0 !important;"><p id="dynamic-signature"></p><p style="font-size:12px"><strong style="font-size:12px"><br><br>Authorised Signatory</strong></p><p style="font-size:12px"><strong>Covai Civil Lab Private Limited</strong></p></td><td width="40%" style="border:none !important;"><p></p><p style="text-align:justify"></p></td><td width="20%" style="border:0 !important;" class="qr-code"><img src="https://files.covaiciviltechlab.com/'+str(obj.invoice_image)+'"></td></tr><tr><td colspan="3" style="border:0 !important;"><hr style="color: #000;"></td></tr><tr style="border-spacing:0.6pt; border:0 !important;"><td colspan="3" style="border:0px !important; border-style:inset; border-width:0.75pt; vertical-align:middle"><p><img alt="Logo" src="https://files.covaiciviltechlab.com/static/test-footer.png" style="width:100%" /></p></td></tr></table></figure>'
            return data

        else:
            return None
        
        '''
        try:

            html_content = obj.report_template

            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the div element by class name and remove it
            div_to_remove = soup.find('tr', class_='header-img-div')
            if div_to_remove:
                div_to_remove.extract()

           
            # Print the modified HTML
            final_html  = soup.prettify()
            return str(final_html)
        except:
            return "sample"

        '''

 
    

    


class Invoice_Serializer1(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    customer_no = serializers.SerializerMethodField()

    class Meta:
        model =  Invoice
        fields = ['id','invoice_no','customer','customer_no']

    def get_customer_no(self,obj):
        return (obj.customer.phone_no)
    
class Test_serializer(serializers.ModelSerializer):
    class Meta:
        model =  Test
        fields = ['id','test_name']


class Pending_Invoice_Serializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    incompleted_test = serializers.SerializerMethodField()

    
    class Meta:
        model =  Invoice
        fields = ['id','customer','project_name','total_amount','advance','balance','invoice_no','fully_paid','incompleted_test']
    
    def get_incompleted_test(self,obj):
        return str(obj.incompleted_test)


class Create_Invoice_File_Serializer(serializers.ModelSerializer):
    class Meta:
        model =  Invoice_File
        fields = ['invoice','file','category','expense']


class Invoice_File_Serializer(serializers.ModelSerializer):
    file_url  = serializers.SerializerMethodField()
    invoice_no  = serializers.SerializerMethodField()
    category_name  = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()
    modified_by  = serializers.StringRelatedField()
    expense_category = serializers.SerializerMethodField()
    expense_user = serializers.SerializerMethodField()
    
    class Meta:
        model =  Invoice_File
        fields = ['id','invoice','file_url','category','invoice_no','category_name','created_by','modified_by','modified_date','created_date','expense','expense_category','expense_user']
        
    def get_invoice_no(self,obj):
        try:
            return obj.invoice.invoice_no
        except:
            return None
    
    def get_category_name(self,obj):
        return str(obj.category)
    
    def get_expense_category(self,obj):
        try:
            return str(obj.expense.expense_category.expense_name)
        except:
            return None
    
    
    def get_expense_user(self,obj):
        try:
            return str(obj.expense.expense_user)
        except:
            return None
    
    def get_file_url(self, obj):
        return "https://files.covaiciviltechlab.com/media/"+str(obj.file)
    

class CustomDateFormatField(serializers.Field):
    def to_representation(self, value):
        # Convert the DateTimeField to a date with a specific format
        return value.strftime('%d-%m-%Y')

class Expense_Entry_Serializer1(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    expense_category = serializers.StringRelatedField()
    date = CustomDateFormatField()

    class Meta:
        model = Expense_Entry
        fields = '__all__'


class Customer_Serializer_For_Invoice(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','customer_name','address1']



class Invoice_Serializer_For_Report(serializers.ModelSerializer):
    incompleted_test = serializers.SerializerMethodField()
    export_date = serializers.SerializerMethodField()


    class Meta:
        model = Invoice
        fields = ['customer_name','customer_gst_no','project_name','invoice_no','date','export_date', 'amount','tds_amount','cgst_tax','sgst_tax','total_amount','cash','cheque_neft','tax_deduction','advance','balance','discount','amount_paid_date','bank','cheque_number','payment_mode','place_of_testing','tax','sales_mode','incompleted_test','upi','completed']


    def get_incompleted_test(self,obj):
        return str(obj.incompleted_test)
    

    def get_export_date(self,obj):
        try:
            return obj.date.strftime("%d-%m-%Y")
        except:
            return ''
    
    
class Invoice_Report(serializers.ModelSerializer):
    incompleted_test = serializers.SerializerMethodField()
    export_date = serializers.SerializerMethodField()
    upi = serializers.SerializerMethodField()
    neft = serializers.SerializerMethodField()
    tds = serializers.SerializerMethodField()
    cheque_neft = serializers.SerializerMethodField()


    class Meta:
        model = Invoice
        fields = ['customer_name','customer_gst_no','project_name','invoice_no','date','export_date', 'amount','cgst_tax','sgst_tax','total_amount','cash','cheque_neft','tds','tax_deduction','advance','balance','discount','amount_paid_date','bank','cheque_number','payment_mode','place_of_testing','tax','sales_mode','incompleted_test','upi','neft','completed','igst_tax']


    def get_incompleted_test(self,obj):
        return str(obj.incompleted_test)
    

    def get_export_date(self,obj):
        try:
            return obj.date.strftime("%d-%m-%Y")
        except:
            return ''
        
    def get_upi(self,obj):

        receipts = list(Receipt.objects.filter(invoice_no__id=obj.id,upi__isnull=False).values('upi'))
        upi_values = [item['upi'] for item in receipts]
        result_string = ', '.join(upi_values)

        return ', '.join(upi_values)
    

    def get_neft(self,obj):

        receipts = list(Receipt.objects.filter(invoice_no__id=obj.id,neft__isnull=False).values('neft'))
        neft_values = [item['neft'] for item in receipts]
        return ', '.join(neft_values)
    
    def get_tds(self,obj):

        receipts = list(Receipt.objects.filter(invoice_no__id=obj.id,tds__isnull=False).values('tds'))
        tds_values = [item['tds'] for item in receipts]
        return ', '.join(tds_values)
    

    def get_cheque_neft (self,obj):

        receipts = list(Receipt.objects.filter(invoice_no__id=obj.id,cheque_number__isnull=False).values('cheque_number'))
        upi_values = [item['cheque_number'] for item in receipts]
        result_string = ', '.join(upi_values)

        return ', '.join(upi_values)
    
    
    


class Invoice_Serializer_For_Print(serializers.ModelSerializer):
    inr =  serializers.SerializerMethodField()
    qr =  serializers.SerializerMethodField()
    date = CustomDateFormatField()


    class Meta:
        model = Invoice
        fields = ['id','qr','date','invoice_no','project_name','invoice_image','customer_name','customer_gst_no','amount','tds_amount','cgst_tax','sgst_tax','total_amount','cash','cheque_neft','tax_deduction','advance','balance','discount','amount_paid_date','bank','cheque_number','payment_mode','inr','tax','place_of_testing']

    def get_inr(self,obj):
        return str(num2words(obj.total_amount-obj.tds_amount)).capitalize()
    
    def get_qr(self,obj):
        if obj.invoice_image:
            return "https://files.covaiciviltechlab.com/"+obj.invoice_image
        else:
            return ""

class Customer_Serializer_For_Print(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['address1','place_of_testing','gstin_no','customer_name']



class Invoice_Test_Serializer_For_Print(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()
    final_html = serializers.SerializerMethodField()
    
    

    class Meta:
        model = Invoice_Test
        fields = ['id','invoice','material_name','test','test_name','qty','price_per_sample','total','invoice_image','final_html']   

    def get_test_name(self,obj):
        return str(obj.test)
    

    def get_material_name(self,obj):
        return str(obj.test.material_name)
    
    def get_qty(self,obj):
        return str(int(obj.quantity))
    
    def get_final_html(self,obj):
        html_content = obj.report_template

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the div element by class name and remove it
        div_to_remove = soup.find('div', class_='header-img-div')
        if div_to_remove:
            div_to_remove.extract()

        # Print the modified HTML
        final_html  = soup.prettify()
        return str(final_html)
    




class Invoice_Serializer_For_Dashboard(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    class Meta:
        model = Invoice
        fields = ['id','invoice_no','total_amount','customer','sales_mode','project_name','discount','tax','advance','balance','place_of_testing']



class Expense_File_Report_Serializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    expense_date = serializers.SerializerMethodField() 
    
    class Meta:
        model = Invoice_File
        fields = ['id','expense','expense_user','expense_amount','expense_date','file']


    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None
    
    def get_expense_date(self,obj):
        return obj.created_date.strftime('%d-%m-%Y')
    

class Invoice_File_Report_Serializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    invoice_date = serializers.SerializerMethodField()
 
    
    class Meta:
        model = Invoice_File
        fields = ['id','invoice_no','invoice_customer','invoice_amount','invoice_date','file']


    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None
    
    def get_invoice_date(self,obj):
        return obj.created_date.strftime('%d-%m-%Y')



class Test_List_Serializer(serializers.ModelSerializer):
    test_name = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()
    qty = serializers.SerializerMethodField()

    
    

    class Meta:
        model = Invoice_Test
        fields = ['id','invoice','invoice_no','material_name','test','test_name','qty','price_per_sample','total','invoice_image','customer','created_date','completed']   

    def get_test_name(self,obj):
        return str(obj.test)
    

    def get_material_name(self,obj):
        return str(obj.test.material_name)
    
    def get_qty(self,obj):
        return str(int(obj.quantity))
    

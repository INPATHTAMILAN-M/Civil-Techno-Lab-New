from django.shortcuts import render,redirect
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status 
from general.models import Material,Expense,Test,Tax
from .models import Expense_Entry,Invoice,SalesMode,Invoice_Test, Invoice_File, Invoice_File_Category, Receipt
from account.models import Customer
#from general.serializers import Material_Serializer1
from .serializers import Create_Expense_Entry_Serializer,Expense_Entry_Serializer,Expense_Serializer1,Create_Invoice_Serializer,Invoice_Serializer,Customer_Serializer1,Sales_mode_Serializer1,Tax_Serializer1,Material_Test_Serializer,Material_Serializer2,Create_Invoice_Test_Serializer,Invoice_Test_Serializer,Invoice_Serializer1,Test_serializer, Pending_Invoice_Serializer, Create_Invoice_File_Serializer, Invoice_File_Serializer, Expense_Entry_Serializer1, Customer_Serializer_For_Invoice, Invoice_Serializer_For_Report, Edit_Invoice_Serializer, Invoice_Serializer_For_Print, Customer_Serializer_For_Print, Invoice_Test_Serializer_For_Print, Invoice_File_Category_Serializer, Invoice_Serializer_For_Dashboard, Receipt_Serializer, Receipt_Serializer_List, Invoice_Report, Expense_File_Report_Serializer, Invoice_File_Report_Serializer, Test_List_Serializer
from django.db.models import Sum, Q
import json
from bs4 import BeautifulSoup
from account.serializers import Employee_Serializer
from account.models import Employee
from datetime import datetime
from general.serializers import Create_Material_Serializer,Test_Serializer1


class Create_Expense_Entry(APIView):
    
    def get(self, request): 
        expense = Expense.objects.all()
     
        expense_serializer = Expense_Serializer1(expense, many=True)

        context = {
                    'expense': expense_serializer.data,
                   
                }
        return Response(context)    

    def post(self, request, *args, **kwargs):
        serializer = Create_Expense_Entry_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user,modified_by=request.user)
            expense_entry = Expense_Entry.objects.get(id=serializer.id)
            serializer = Expense_Entry_Serializer(expense_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class List_Expense_Entry(APIView):

    def get(self, request, *args, **kwargs):
        expense_entries = Expense_Entry.objects.all().order_by('-id')
        serializer = Expense_Entry_Serializer(expense_entries, many=True)
        return Response(serializer.data)
    


    def post(self, request):
        expense_user = request.data['expense_user']
        expense_category = request.data['expense_category']
        from_date = request.data['from_date']
        to_date = request.data['to_date']

        filters = { }

        if expense_user:
            filters['expense_user__icontains'] = expense_user
        if expense_category:
            filters['expense_category__id'] = expense_category
        if from_date:
            filters['date__gte'] = datetime.strptime(from_date, '%Y-%m-%d').date()
        if to_date:
            filters['date__lte'] = datetime.strptime(to_date, '%Y-%m-%d').date()        

        expense_entries = Expense_Entry.objects.filter(**filters).order_by('-id')
        serializer = Expense_Entry_Serializer(expense_entries, many=True)
        return Response(serializer.data)

       
    

class Edit_Expense_Entry(APIView):

    def get(self, request,id): 
        expense = Expense.objects.all()
        expense_serializer = Expense_Serializer1(expense, many=True)      
        context = {
                    'expense': expense_serializer.data,
                }
        return Response(context)    

    def put(self, request, id):
        expense_entry = Expense_Entry.objects.get(id=id)
        serializer = Create_Expense_Entry_Serializer(expense_entry, data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save()
            expense_entry = Expense_Entry.objects.get(id=serializer.id)
            serializer = Expense_Entry_Serializer(expense_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class Delete_Expense_Entry(APIView):

    def delete(self, request, id):
        data = dict()
        try:
            expense_entry = Expense_Entry.objects.get(id=id)
        except Expense_Entry.DoesNotExist:
            data['valid'] = False
            data['error'] = "Expense Entry not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        expense_entry.delete()
        data['deleted'] = True
        return Response(data)


class Create_Invoice(APIView):
    def get(self, request): 
        customer = Customer.objects.all()
        sales_mode = SalesMode.objects.all()
        taxs = Tax.objects.all()
        customer_serializer = Customer_Serializer1(customer, many=True)
        sales_mode_serializer = Sales_mode_Serializer1(sales_mode, many=True)
        tax_serializer = Tax_Serializer1(taxs, many=True)
        
        context = {
                    'customer': customer_serializer.data,
                    'sales_mode':sales_mode_serializer.data,
                    'taxs': tax_serializer.data,              
                }
        return Response(context)    

    def post(self, request, *args, **kwargs):
        serializer = Create_Invoice_Serializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user,modified_by=request.user)
            invoice = Invoice.objects.get(id=serializer.id)


            if Invoice.objects.filter(invoice_no__isnull=False).exists():
                last_invoice  = Invoice.objects.filter(invoice_no__isnull=False).last()
                last_invoice_no = int(last_invoice.invoice_no)
                if len(str(last_invoice_no)) == 1 and not last_invoice_no == 9:
                    invoice_no = "00"+str(last_invoice_no+1)
                else:
                    invoice_no = "0"+str(last_invoice_no+1)

                invoice.invoice_no=invoice_no
                invoice.save()

            else:
                invoice_no = "001"
                invoice.invoice_no=invoice_no
                invoice.save()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            # Add data to the QR code
            qr.add_data("https://app.covaiciviltechlab.com/invoice/viewinvoicereport?id="+str(serializer.id))
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image to a file
            invoice_img_path  = "media/invoice/invoice_"+invoice_no+".png"
            img.save(invoice_img_path)
        
            invoice  = Invoice.objects.get(id=serializer.id)
            invoice.invoice_image = invoice_img_path
            if invoice.customer.place_of_testing:
                invoice.place_of_testing = invoice.customer.place_of_testing
            invoice.save()

            return Response({'id':invoice.id,},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class List_Invoice(APIView):
    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.all().order_by('-id')
        serializer = Invoice_Serializer(invoices, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        #invoice_no = request.data['invoice_no']
        from_date = request.data['from_date']
        to_date = request.data['to_date']
        customer = request.data['customer']
        project_name  = request.data['project_name']
        completed = request.data['completed']

        filters = {}

        if customer:
            filters['customer__id'] = customer
        if project_name:
            filters['project_name__icontains'] = project_name
        if from_date:
            filters['date__gte'] = datetime.strptime(from_date, '%Y-%m-%d').date()
        if to_date:
            filters['date__lte'] = datetime.strptime(to_date, '%Y-%m-%d').date()
        if completed:
            filters['completed'] = completed

        invoices = Invoice.objects.filter(**filters).order_by('-id')

        serializer = Invoice_Serializer(invoices, many=True)
        return Response(serializer.data)
    




        


class Edit_Invoice(APIView):

    def get(self, request,id): 
        
        sales_mode = SalesMode.objects.all()
        taxs = Tax.objects.filter(tax_status="E")
        
        sales_mode_serializer = Sales_mode_Serializer1(sales_mode, many=True)
        tax_serializer = Tax_Serializer1(taxs, many=True)

        invoice_object = Invoice.objects.get(id=id)
        invoice = Invoice_Serializer_For_Report(invoice_object) 
        customer = Customer.objects.get(id=invoice_object.customer.id)
        customer = Customer_Serializer1(customer)

        invoice_tests = Invoice_Test.objects.filter(invoice__id=invoice_object.id)
        invoice_tests = Invoice_Test_Serializer(invoice_tests, many=True)

        customers = Customer.objects.all()
        customers = Customer_Serializer1(customers,many=True)

        payments = Receipt.objects.filter(invoice_no=invoice_object)
        payments = Receipt_Serializer_List(payments,many=True)
        payment_mode_choices = [
            {
                "id":1,
                "name":"cash",
                "value":"cash"
                },
                {
                      "id":2,
                "name":"cheque",
                "value":"cheque",

                },
                {
                     "id":3,
                "name":"UPI",
                "value":"upi",

                },

                {
                     "id":4,
                "name":"NEFT",
                "value":"neft",

                },
                {
                    "id":5,
                    "name":"TDS",
                    "value":"tds"
                }
                
                ]
        
        context = {
                    'invoice':invoice.data,
                    'customer': customer.data,
                    'invoice_tests':invoice_tests.data,                    
                    'sales_mode':sales_mode_serializer.data,
                    'taxs': tax_serializer.data, 
                    'customers': customers.data,  
                    'payment_mode_choices':payment_mode_choices,
                    'payments':payments.data,
                             
                }
        return Response(context)

    def put(self, request, id):
        invoice = Invoice.objects.get(id=id)
        serializer = Edit_Invoice_Serializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(modified_by=request.user)
            invoice = Invoice.objects.get(id=serializer.id)
            if int(invoice.total_amount) == int(invoice.advance):
                invoice.fully_paid = True
            else:
                invoice.fully_paid = False
            invoice = invoice.save()

            invoice = Invoice.objects.get(id=serializer.id)


            serializer = Invoice_Serializer_For_Report(invoice)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class Delete_Invoice(APIView):

    def delete(self, request, id):
        data = dict()
        try:
            invoice = Invoice.objects.get(id=id)
        except Invoice.DoesNotExist:
            data['valid'] = False
            data['error'] = "Invoice not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        invoice.delete()
        data['deleted'] = True
        return Response(data)


class Material_Test(APIView):
    def get(self, request, *args, **kwargs):
        materials = Material.objects.all()
        tests = Test.objects.all()
        material_serializer = Material_Serializer2(materials,many=True)
        test_serializer = Material_Test_Serializer(tests,many=True)
        context = {
                    'materials': material_serializer.data,
                    'tests': test_serializer.data,
                }
        return Response(context) 

class Create_Invoice_Test(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        tests = Test.objects.all()
        invoice_serializer = Invoice_Serializer1(invoices,many=True)
        test_serializer = Test_serializer(tests,many=True)
        context = {
                    'invoices': invoice_serializer.data,
                    'tests': test_serializer.data,
                }
        return Response(context) 

    def post(self, request, *args, **kwargs):
        serializer = Create_Invoice_Test_Serializer(data=request.data,many=True)
        if serializer.is_valid():            
            serializer = serializer.save(created_by=request.user, modified_by=request.user)

            for i_test in serializer:
               
                data = i_test.test.material_name.template

                data = data.replace('<td colspan="2">&nbsp;</td>', '<td colspan="2"><img alt="Logo" src="https://files.covaiciviltechlab.com/static/header.gif" style="width:100%" /> </td>',1)

                order_no = 'Test Order: '+str(i_test.invoice.invoice_no)
                data = data.replace('Test Order', order_no)
                cus_address = '<p>'+i_test.invoice.customer.customer_name+'</p><p>'+i_test.invoice.customer.address1+'</p>'
                data = data.replace('CUSTOMERDETAILS', cus_address)


                

                date = 'Date : '+ str(i_test.created_date.strftime("%d-%m-%Y"))

                data = data.replace('Date :', date)

                data = data.replace('Place of Testing Name', str(i_test.invoice.place_of_testing))
                data = data.replace('Project Name', str(i_test.invoice.project_name))

                #data = data + '<figure class="table"><table cellpadding="0" cellspacing="1" border="0" style="border:0 !important; border-spacing:0.6pt; border:0.75pt outset #000; width:100%"><tr><td width="40%" style="border:0 !important;"><p><img src="http://files.covaiciviltechlab.com/static/G.Govardhan - Manager.jpeg"  height="150px" width="150px"></p><p style="text-align:justify"><strong>COVAI CIVIL TECH LAB </strong></p><p style="text-align:justify"><strong>G.GOVARDHAN,.BE (CIVIL) </strong></p><p style="text-align:justify"><strong>MANAGER</strong></p></td><td width="40%"  style="border:0 !important;"><p id="dynamic-signature">Tester signature</p><p style="text-align:justify"><strong> Tester Name </strong></p><p style="text-align:justify"><strong>COVAI CIVIL TECH LAB</strong></p> </td> <td width="20%"  style="border:0 !important;" class="qr-code"> qr code </td> </tr> <tr><td colspan="3" style="border:0 !important;"> <hr style="color: #000;"></td></tr> <tr style="border-spacing:0.6pt; border:0 !important;"> <td colspan="3" style="border:0px !important; border-style:inset; border-width:0.75pt; vertical-align:middle"> <p><img alt="Logo" src="http://files.covaiciviltechlab.com/static/test-footer.png" style="width:100%" /></p> </td> </tr> </table></figure>'



                '''
                html_content = i_test.test.material_name.template

                # Parse the HTML content
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find the div element by class name and remove it
             
                div_to_remove = soup.find('tr', class_='header-img-div')
                if div_to_remove:
                    div_to_remove.extract()

            

                div_to_modify = soup.find('span', class_='order_date')

                # Check if the div with the specified class exists
                if div_to_modify:
                    # Modify the content of the div
                    div_to_modify.string = "Date :"+str(i_test.created_date)
            
                div_to_modify = soup.find('span', class_='order_no')

                # Check if the div with the specified class exists
                if div_to_modify:
                    # Modify the content of the div
                    div_to_modify.string = "Test Order No:"+str(i_test.invoice.invoice_no)
                
                div_to_modify = soup.find('span', class_='customer-div')

                # Check if the div with the specified class exists
                if div_to_modify:
                    # Modify the content of the div
                    div_to_modify.string = str(i_test.invoice.customer.address1)

                

                div_to_modify = soup.find('td', class_='qr-code')

                # Check if the div with the specified class exists
                if div_to_modify:
                    # Modify the content of the div
                    img_element = soup.new_tag('img', src='http://files.covaiciviltechlab.com/media/invoice_test/invoice_'+str(i_test.id)+'.png', height='120', width='120')


                    div_to_modify.append(img_element)


                div_to_modify = soup.find('span', class_='project-div')

                # Check if the div with the specified class exists
                if div_to_modify:
                    # Modify the content of the div
                    div_to_modify.string = str(i_test.invoice.project_name)

                # Print the modified HTML
                final_html  = soup.prettify()
                i_test.report_template = final_html

                '''

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )

                # Add data to the QR code
                qr_code = "https://app.covaiciviltechlab.com/invoice/viewtestreport?id="+str(i_test.id)
                qr.add_data(qr_code)
                qr.make(fit=True)

                # Create an image from the QR code
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the image to a file
                invoice_img_path  = "media/invoice_test/invoice_"+str(i_test.id)+".png"
                img.save(invoice_img_path)
            
        
                i_test.invoice_image = invoice_img_path
                 
                data = data.replace('qr code', '<img height="120", width="120" src="https://files.covaiciviltechlab.com/'+invoice_img_path+'">')
             
                i_test.report_template = data

                i_test.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class List_Invoice_Test(APIView):
    def get(self, request,id, *args, **kwargs):
        invoice_tests = Invoice_Test.objects.filter(invoice__id=id)
        serializer = Invoice_Test_Serializer(invoice_tests, many=True)
        return Response(serializer.data)

class Edit_Invoice_Test(APIView):

    def get(self, request,id):
        invoices = Invoice.objects.all()
        tests = Test.objects.all()
        invoice_serializer = Invoice_Serializer1(invoices,many=True)
        test_serializer = Test_serializer(tests,many=True)
        invoice_tests = Invoice_Test.objects.filter(invoice__id=id)
        invoice_tests = Invoice_Test_Serializer(invoice_tests, many=True)
        context = {
                    'invoices': invoice_serializer.data,
                    'tests': test_serializer.data,
                    'invoice_tests':invoice_tests.data,
                }
        return Response(context)

    def put(self, request, id):
        invoice_test = Invoice_Test.objects.get(id=id)
        serializer = Create_Invoice_Test_Serializer(invoice_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer = serializer.save(modified_by=request.user)
            invoice_test = Invoice_Test.objects.get(id=serializer.id)
            serializer = Invoice_Test_Serializer(invoice_test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class Delete_Invoice_Test(APIView):
    def delete(self, request, id):
        data = dict()
        try:
            invoice_test = Invoice_Test.objects.get(id=id)
        except Invoice_Test.DoesNotExist:
            data['valid'] = False
            data['error'] = "Invoice Test not found"
            return Response(data, status=status.HTTP_404_NOT_FOUND)
            
        invoice_test.delete()
        data['deleted'] = True
        return Response(data)


class Pending_Payment(APIView):
    def get(self, request):
        invoices = Invoice.objects.filter(fully_paid=False).order_by('-id')
        invoices = Pending_Invoice_Serializer(invoices,many=True)
        context = {
            'pending_payments':invoices.data,
        }
        return Response(context)
    

    def post(self, request):
        #invoice_no = request.data['invoice_no']
        from_date = request.data['from_date']
        to_date = request.data['to_date']
        customer = request.data['customer']
        project_name  = request.data['project_name']
        invoice_no = request.data['invoice_no']

        filters = {
            'completed':'No',
        }

        if customer:
            filters['customer__id'] = customer
        if project_name:
            filters['project_name__icontains'] = project_name
        if from_date:
            filters['date__gte'] = datetime.strptime(from_date, '%Y-%m-%d').date()
        if to_date:
            filters['date__lte'] = datetime.strptime(to_date, '%Y-%m-%d').date()
        if invoice_no:
            filters['invoice_no__icontains'] = invoice_no

        invoices = Invoice.objects.filter(**filters)
   

        invoices = Invoice.objects.filter(**filters)

        serializer = Pending_Invoice_Serializer(invoices, many=True)
        context = {
            'pending_payments':serializer.data,
        }
        return Response(context)
    





class Create_Invoice_File_Upload(APIView):
    def get(self, request):
        invoices = Invoice.objects.filter(invoice_no__isnull=False).order_by('-id')
        invoice_serializer = Invoice_Serializer1(invoices,many=True)
        expense_entries = Expense_Entry.objects.all().order_by('-id')
        expense_entries = Expense_Entry_Serializer(expense_entries,many=True)

        categories = Invoice_File_Category.objects.all()
        categories = Invoice_File_Category_Serializer(categories,many=True)
        
        context = {
                    'invoices': invoice_serializer.data,
                    'categories':categories.data,
                    'expense_entries':expense_entries.data,
                  
                }
        return Response(context) 

    def post(self, request, *args, **kwargs):
        serializer = Create_Invoice_File_Serializer(data=request.data,partial=True)
        if serializer.is_valid():
            serializer = serializer.save(created_by=request.user,modified_by=request.user)
            files = Invoice_File.objects.get(id=serializer.id)
            serializer = Invoice_File_Serializer(files)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Manage_Invoice_File_Upload(APIView):

    def get(self,request):
        files = Invoice_File.objects.all().order_by('-id')
        files = Invoice_File_Serializer(files,many=True)

        context = {
            'invoice_files':files.data,
        }
        return Response(context)

    def delete(self,request,id):
        data = dict()
        try:
            file = Invoice_File.objects.get(id=id)            
        except ObjectDoesNotExist:
            data['valid'] = False
            data['error'] = "Invoice File not found"
            return Response(data,status=status.HTTP_404_NOT_FOUND)       
        file.delete()
        data['deleted'] = True

        return Response(data)
    

    def post(self, request):
        #invoice_no = request.data['invoice_no']
        from_date = request.data['from_date']
        to_date = request.data['to_date']
        category = request.data['category']
        invoice_no = request.data['invoice_no']

        filters = {
           
        }

        if category:
            filters['category__id'] = category

        if from_date:
            filters['created_date__gte'] = from_date
        if to_date:
            filters['created_date__lte'] = to_date
        if invoice_no:
            filters['invoice__invoice_no__icontains'] = invoice_no

        files = Invoice_File.objects.filter(**filters).order_by('-id')

        files = Invoice_File_Serializer(files,many=True)

        context = {
            'invoice_files':files.data,
        }
        return Response(context)
    



class Update_Invoice_File_Upload(APIView):

    def get(self, request,id):
        invoice_file = Invoice_File.objects.get(id=id)
        invoice_file = Invoice_File_Serializer(invoice_file)
        context = {
                    'invoice_file': invoice_file.data,                  
                }
        return Response(context) 


    def put(self, request, id):    
        file  = Invoice_File.objects.get(id=id)
        serializer = Create_Invoice_File_Serializer(file,data=request.data,partial=True)
        if serializer.is_valid():         
            serializer = serializer.save(modified_by=request.user)
            file = Invoice_File.objects.get(id=serializer.id)
            serializer = Invoice_File_Serializer(file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class Expense_Report(APIView):

    def get(self, request):
        expense_entries = Expense_Entry.objects.all().order_by('-id')
        serializer = Expense_Entry_Serializer1(expense_entries, many=True)
        total = Expense_Entry.objects.aggregate(Sum('amount'))
        expense = Expense.objects.all()
        expense = Expense_Serializer1(expense,many=True)
        context  = {
            'reports':serializer.data,
            'total':total,
            'expense_category':expense.data,
        }
        return Response(context)
    

    def post(self, request):
        expense_user = request.data['expense_user']
        expense_category = request.data['expense_category']
        from_date = request.data['from_date']
        to_date = request.data['to_date']

        expense_entries = Expense_Entry.objects.all().order_by('-id')


        if expense_category:
            expense_entries = expense_entries.filter(expense_category__id = expense_category)            
        if expense_user:
            expense_entries = expense_entries.filter(Q(expense_user__icontains = expense_user))
        if from_date:
            expense_entries = expense_entries.filter(date__gte=from_date)
        if to_date:
            expense_entries = expense_entries.filter(date__lte=to_date)


        serializer = Expense_Entry_Serializer1(expense_entries, many=True)


        context  = {
            'reports':serializer.data,
        }
        return Response(context)

       
    

class Sale_Report(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = Customer_Serializer_For_Invoice(customers, many=True)     
        context  = {
            'reports':serializer.data,
        }
        return Response(context)
    

    def post(self, request):
        project_name = request.data['project_name']
        from_date = request.data['from_date']
        to_date = request.data['to_date']
        customer = request.data['customer']
        invoices  = Invoice.objects.filter().order_by('-id')
        if customer:
            invoices = invoices.filter(customer__id = customer)            
        if project_name:
            invoices = invoices.filter(Q(project_name__icontains = project_name))
        if from_date:
            invoices = invoices.filter(date__gte=from_date)
        if to_date:
            invoices = invoices.filter(date__lte=to_date)

        serializer = Invoice_Report(invoices, many=True)     
        context  = {
            'reports':serializer.data,
        }
        return Response(context)


class Edit_Invoice_Test_Template(APIView):

    def get(self, request,id):
    
        invoice_test_object = Invoice_Test.objects.get(id=id)
        invoice_test = Invoice_Test_Serializer(invoice_test_object)
        invoice = Invoice.objects.get(id=invoice_test_object.invoice.id)
        invoice_serializer = Invoice_Serializer_For_Print(invoice)
        employees = Employee.objects.filter(role__isnull=False,signature__isnull=False)
        signatures = Employee_Serializer(employees,many=True)
        context = {
                    'invoice': invoice_serializer.data,                
                    'invoice_test':invoice_test.data,
                    'signatures':signatures.data,
                }
        return Response(context)

    def put(self, request, id):
        invoice_test = Invoice_Test.objects.get(id=id)
        serializer = Invoice_Test_Serializer(invoice_test, data=request.data, partial=True)
        if serializer.is_valid():
            serializer = serializer.save()

            if serializer.signature:           
                soup = BeautifulSoup(serializer.report_template, 'html.parser')

                div_to_modify = soup.find('p', class_='dynamic-signature')

                # Check if the div with the specified class exists
                if div_to_modify:
                    # Modify the content of the div
                    img_element = soup.new_tag('img', src='https://files.covaiciviltechlab.com/media/'+str(serializer.signature.signature))


                    div_to_modify.replace_with(img_element)

                final_html  = soup.prettify()
                serializer.report_template = final_html
                serializer.save()

            invoice_test = Invoice_Test.objects.get(id=serializer.id)
            serializer = Invoice_Test_Serializer(invoice_test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

        


class Preview_Invoice_Test_Template(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request,id):
    
        invoice_test_object = Invoice_Test.objects.get(id=id)
        invoice_test = Invoice_Test_Serializer(invoice_test_object)
        invoice = Invoice.objects.get(id=invoice_test_object.invoice.id)
        invoice_serializer = Invoice_Serializer_For_Print(invoice)
        employees = Employee.objects.filter(role__isnull=False,signature__isnull=False)
        signatures = Employee_Serializer(employees,many=True)
        context = {
                    'invoice': invoice_serializer.data,                
                    'invoice_test':invoice_test.data,
                    'signatures':signatures.data,
                }
        return Response(context)

  
     

import qrcode

def qr(request):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data("http://127.0.0.1:8000/create_invoice/")
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    img.save("some_file.png")


class Print_Invoice(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request,pk):
        invoice = Invoice.objects.get(id=pk)
        serializer = Invoice_Serializer_For_Print(invoice)
        customer = Customer.objects.get(id=invoice.customer.id)
        customer = Customer_Serializer_For_Print(customer)
        invoice_tests = Invoice_Test.objects.filter(invoice__id=pk)
        invoice_tests = Invoice_Test_Serializer_For_Print(invoice_tests, many=True)
        taxs = Tax.objects.all()
        tax_serializer = Tax_Serializer1(taxs, many=True)
        context = {
            'invoice':serializer.data,
            'customer':customer.data,
            'invoice_tests':invoice_tests.data,
            'taxes':tax_serializer.data,
        }
        return Response(context)


from datetime import datetime, timedelta 

class Dashboard(APIView):

    def get(self, request):
        year = datetime.now().year
        month = datetime.now().month
        this_month_name = datetime.now().strftime('%B')
        this_month = datetime.now().month
        pending_payment_count = Invoice.objects.filter(fully_paid=False).count()

        this_month_generated_invoice  = Invoice.objects.filter(created_date__year=year,created_date__month=month).count()
        all_invoice  = Invoice.objects.filter().count()

        this_month_generated_incompleted_invoice  = Invoice.objects.filter(completed="No",created_date__year=year,created_date__month=month).count()
        incompleted_invoice_count  = Invoice.objects.filter(completed="No").count()
        this_month_generated_incompleted_test  = Invoice_Test.objects.filter(completed="No",created_date__year=year,created_date__month=month).count()
        incompleted_test_count  = Invoice_Test.objects.filter(completed="No").count()

        this_month_pending_payment_count = invoices = Invoice.objects.filter(fully_paid=False,created_date__year=year,created_date__month=month).count()
        this_month_expense_total = Expense_Entry.objects.filter(created_date__year=year,created_date__month=month).aggregate(Sum('amount'))
        this_month_expense_entry_count = Expense_Entry.objects.filter(created_date__year=year,created_date__month=month).count()
        customer_count = Customer.objects.all().count()
        this_month_customer_count = Customer.objects.filter(created_date__year=year,created_date__month=month).count()
        category_wise_amounts = Expense_Entry.objects.values('expense_category__expense_name').annotate(total_amount=Sum('amount'))
        this_month_expense_count = Expense_Entry.objects.filter(created_date__year=year,created_date__month=month).count()
        total_expense_count = Expense_Entry.objects.filter().count()

        pending_payment = Invoice.objects.filter(fully_paid=False).aggregate(Sum('balance'))

        pending_payment_this_month = Invoice.objects.filter(created_date__year=year,created_date__month=month,fully_paid=False).aggregate(Sum('balance'))
        
        invoices = Invoice.objects.all().order_by('-id')[:10]
        invoices = Invoice_Serializer_For_Dashboard(invoices, many=True)
                



        today = datetime.today()

        # Adjust the current month for financial year
        if today.month in [1, 2, 3]:
            current_month = today.month + 9
            current_year = today.year - 1
        else:
            current_month = today.month - 3
            current_year = today.year

        # Generate dates for the last 12 months in financial year month format
        last_12_months = [datetime(current_year, (current_month - i) % 12 + 1, 1) for i in range(12)]



        
        months_name = []
        total_amount = []
        paid_amount = []
        banlance_amount = []
        expense_amount_list = []

        expenses = Expense_Entry.objects.all().order_by('-id')[:10]
        expenses = Expense_Entry_Serializer(expenses, many=True)
        month_list = []

        for month in last_12_months:
            months_name.append(month.strftime('%B'))
            month_list.append(month.month)
            amount = Invoice.objects.filter(created_date__year=year,created_date__month=month.month).aggregate(Sum('total_amount'))
            if amount['total_amount__sum']:                
                total_amount.append(amount['total_amount__sum'])
            else:
                total_amount.append(0)
            advance = Invoice.objects.filter(created_date__year=year,created_date__month=month.month).aggregate(Sum('advance'))
            if advance['advance__sum']:                
                paid_amount.append(advance['advance__sum'])
            else:
                paid_amount.append(0)                

            balance = Invoice.objects.filter(created_date__year=year,created_date__month=month.month).aggregate(Sum('balance'))
            if balance['balance__sum']:
                banlance_amount.append(balance['balance__sum'])
            else:
                banlance_amount.append(0)

            expense_amount = Expense_Entry.objects.filter(created_date__year=year,created_date__month=month.month).aggregate(Sum('amount'))
            if expense_amount['amount__sum']:
                expense_amount_list.append(expense_amount['amount__sum'])
            else:
                expense_amount_list.append(0)
        
        expense_amount_sum  = sum(expense_amount_list)
 
        tis_month_amount = Invoice.objects.filter(created_date__year=year,created_date__month=this_month).aggregate(Sum('total_amount'))
        if tis_month_amount['total_amount__sum']:                
            tis_month_amount = tis_month_amount['total_amount__sum']
        else:
            tis_month_amount = 0
        tis_month_advance = Invoice.objects.filter(created_date__year=year,created_date__month=this_month).aggregate(Sum('advance'))
        if tis_month_advance['advance__sum']:                
            tis_month_advance = tis_month_advance['advance__sum']
        else:
            tis_month_advance = 0              

        tis_month_balance = Invoice.objects.filter(created_date__year=year,created_date__month=this_month).aggregate(Sum('balance'))
        if tis_month_balance['balance__sum']:
            tis_month_balance = tis_month_balance['balance__sum']
        else:
            tis_month_balance = 0
        
        payments  = [tis_month_amount,tis_month_advance,tis_month_balance]
        payments_sum = sum(payments)

        expenses_list = Expense.objects.all()

        expenses_name = []
        expenses_data = []

        for expense in expenses_list:
            expenses_name.append(str(expense))
            total = Expense_Entry.objects.filter(expense_category=expense,created_date__month__in=month_list).aggregate(Sum('amount'))
            if total['amount__sum']:
                expenses_data.append(total['amount__sum'])
            else:
                expenses_data.append(0)



        context = {
            'this_month_generated_incompleted_invoice':this_month_generated_incompleted_invoice,
            'incompleted_invoice_count':incompleted_invoice_count,
            'this_month_generated_incompleted_test':this_month_generated_incompleted_test,
            'incompleted_test_count':incompleted_test_count,
            'pending_payment_count':pending_payment_count,
            'this_month_generated_invoice':this_month_generated_invoice,
            'this_month_pending_payment_count':this_month_pending_payment_count,
            'this_month_expense_total':this_month_expense_total['amount__sum'],
            'this_month_expense_entry_count':this_month_expense_entry_count,
            'customer_count':customer_count,
            'this_month_customer_count':this_month_customer_count,
            'category_wise_amounts':category_wise_amounts,
            'all_invoice':all_invoice,
            'this_month_expense_count':this_month_expense_count,
            'total_expense_count':total_expense_count,
            'pending_payment':pending_payment['balance__sum'],
            'pending_payment_this_month':pending_payment_this_month['balance__sum'],
            'months_name':months_name,
            'total_amount':total_amount,
            'paid_amount':paid_amount,
            'banlance_amount':banlance_amount,
            'payments':payments,
            'this_month_name':this_month_name,
            'invoices':invoices.data,
            'expenses':expenses.data,
            'expense_amount_list':expense_amount_list,
            'expense_amount_sum':expense_amount_sum,
            'payments_sum':tis_month_amount,
            'expenses_name':expenses_name,
            'expenses_data':expenses_data,

        }
        return Response(context)
    

class Add_Payment(APIView):

    def post(self, request,pk, *args, **kwargs):
        serializer = Receipt_Serializer(data=request.data)
        invoice = Invoice.objects.get(id=pk)
        if serializer.is_valid():            
            serializer = serializer.save(invoice_no=invoice,created_by=request.user, modified_by=request.user)

            payments = Receipt.objects.filter(invoice_no=pk)
            payments = Receipt_Serializer_List(payments,many=True)
            context = {
                'payments':payments.data
            }

            
            return Response(context,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Edit_Payment(APIView):

    def put(self, request,pk, *args, **kwargs):
        receipt = Receipt.objects.get(id=pk)
        serializer = Receipt_Serializer(receipt,data=request.data)
        if serializer.is_valid():            
            serializer = serializer.save(modified_by=request.user)
            payments = Receipt.objects.filter(invoice_no=receipt.invoice_no)
            payments = Receipt_Serializer_List(payments,many=True)
            context = {
                'payments':payments.data
            }            
            return Response(context,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Delete_Payment(APIView):

    def delete(self,request,id):
        data = dict()
        try:
            receipt = Receipt.objects.get(id=id)
            invoice_no =  receipt.invoice_no  
            receipt.delete()
            payments = Receipt.objects.filter(invoice_no=invoice_no)
            payments = Receipt_Serializer_List(payments,many=True)
            context = {
                'payments':payments.data
            } 
            return Response(context)


        except ObjectDoesNotExist:
            data['valid'] = False
            data['error'] = "Payment not found"
            return Response(data,status=status.HTTP_404_NOT_FOUND)       
        

class Expense_File_Report(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = Customer_Serializer_For_Invoice(customers, many=True)     
        context  = {
            'reports':serializer.data,
        }
        return Response(context)
    

    def post(self, request):
        #invoice_no = request.data['invoice_no']
        from_date = request.data['from_date']
        to_date = request.data['to_date']
      
        invoicefiles  = Invoice_File.objects.filter(category__name="Expense",expense__isnull=False).order_by('-id')

        '''
        if invoice_no:
            invoices = invoicefiles.filter(invoice__invoice_no=invoice_no)            
        if project_name:
            invoices = invoices.filter(Q(project_name__icontains = project_name))
        '''

        if from_date:
            invoicefiles = invoicefiles.filter(expense__date__gte=from_date)
        if to_date:
            invoicefiles = invoicefiles.filter(expense__date__lte=to_date)

        serializer = Expense_File_Report_Serializer(invoicefiles, many=True,context={'request':request})     
        context  = {
            'reports':serializer.data,
        }
        return Response(context)


    


class Invoice_File_Report(APIView):

    def get(self, request):
        customers = Customer.objects.all()
        serializer = Customer_Serializer_For_Invoice(customers, many=True)     
        context  = {
            'reports':serializer.data,
        }
        return Response(context)
    

    def post(self, request):
        #invoice_no = request.data['invoice_no']
        from_date = request.data['from_date']
        to_date = request.data['to_date']
      
        invoicefiles  = Invoice_File.objects.filter(category__name="Invoice",invoice__isnull=False).order_by('-id')

        '''
        if invoice_no:
            invoices = invoicefiles.filter(invoice__invoice_no=invoice_no)            
        if project_name:
            invoices = invoices.filter(Q(project_name__icontains = project_name))
        '''

        if from_date:
            invoicefiles = invoicefiles.filter(invoice__date__gte=from_date)
        if to_date:
            invoicefiles = invoicefiles.filter(invoice__date__lte=to_date)

        serializer = Invoice_File_Report_Serializer(invoicefiles, many=True,context={'request':request})     
        context  = {
            'reports':serializer.data,
        }
        return Response(context)
    


class Test_List(APIView):

    def get(self, request):
        materials = Material.objects.all()
        tests = Test.objects.all()
        materials = Create_Material_Serializer(materials,many=True)
        test_data = Test_Serializer1(tests,many=True)

        tests = Invoice_Test.objects.all()
        serializer = Test_List_Serializer(tests,many=True)
        customers = Customer.objects.all()
        customers = Customer_Serializer1(customers,many=True)

        context  = {
            'reports':serializer.data,
            'materials':materials.data,
            'tests':test_data.data,
            'customers':customers.data,
        }
        return Response(context)
    
    def post(self, request):
        from_date = request.data['from_date']
        to_date = request.data['to_date']
        material = request.data['material']
        test = request.data['test']
        customer =  request.data['customer']



        filters = {}

        if customer:
            filters['invoice__customer__id'] = customer
        if test:
            filters['test__id'] = test
        if material:
            filters['test__material_name__id'] = material
        if from_date:
            filters['created_date__gte'] = datetime.strptime(from_date, '%Y-%m-%d').date()
        if to_date:
            filters['created_date__lte'] = datetime.strptime(to_date, '%Y-%m-%d').date()

        tests = Invoice_Test.objects.filter(**filters).order_by('-id')
        serializer = Test_List_Serializer(tests,many=True)
        context  = {
            'reports':serializer.data,
        
        }
        return Response(context)
        




    


    

from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('create_expense_entry/', views.Create_Expense_Entry.as_view(), name='create_expense_entry'),
    path('expense_entry_list/', views.List_Expense_Entry.as_view(), name='expense_entry_list'),
    path('edit_expense_entry/<int:id>/', views.Edit_Expense_Entry.as_view(), name='edit_expense_entry'),
    path('delete_expense_entry/<int:id>/', views.Delete_Expense_Entry.as_view(), name='delete_expense_entry'),

    path('create_invoice/', views.Create_Invoice.as_view(), name='create_invoice'),
    path('invoice_list/', views.List_Invoice.as_view(), name='invoice_list'),
    path('edit_invoice/<int:id>/', views.Edit_Invoice.as_view(), name='edit_invoice'),
    path('delete_invoice/<int:id>/', views.Delete_Invoice.as_view(), name='delete_invoice'),

    path('get_material_test/', views.Material_Test.as_view(), name='material_test'),
    path('create_invoice_test/', views.Create_Invoice_Test.as_view(), name='create_invoice_test'),
    path('invoice_test_list/<int:id>/', views.List_Invoice_Test.as_view(), name='invoice_test_list'),
    path('edit_invoice_test/<int:id>/', views.Edit_Invoice_Test.as_view(), name='edit_invoice_test'),
    path('delete_invoice_test/<int:id>/', views.Delete_Invoice_Test.as_view(), name='delete_invoice_test'),

    path('edit_invoice_test_template/<int:id>/', views.Edit_Invoice_Test_Template.as_view(), name='edit_invoice_test_template'),

   path('preview_invoice_test_template/<int:id>/', views.Preview_Invoice_Test_Template.as_view(), name='preview_invoice_test_template'),


    #madhan
    path('pending_payment/', views.Pending_Payment.as_view(), name='pending payment'),

    
    #invoice file upload
    path('create_invoice_file_upload/', views.Create_Invoice_File_Upload.as_view(), name='create_invoice_file_upload'),
    path('invoice_file_upload_list/', views.Manage_Invoice_File_Upload.as_view(), name='invoice_file_upload_list'),
    path('edit_invoice_file_upload/<int:id>/', views.Update_Invoice_File_Upload.as_view(), name='edit_invoice_file_upload'),
    path('delete_invoice_file_upload/<int:id>/', views.Manage_Invoice_File_Upload.as_view(), name='delete_invoice_file_upload'),
    
    path('expense_report/', views.Expense_Report.as_view(), name='expense_report'),


    path('sale_report/', views.Sale_Report.as_view(), name='sale_report'),

    path('qr/', views.qr, name='qr'),


    path('print_invoice/<int:pk>/', views.Print_Invoice.as_view(), name='Print_invoice'),

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),


    path('add_payment/<int:pk>/', views.Add_Payment.as_view(), name='add_payment'),
    path('edit_payment/<int:pk>/', views.Edit_Payment.as_view(), name='edit_payment'),
    path('delete_payment/<int:id>/', views.Delete_Payment.as_view(), name='delete_payment'),


    path('expense_file_report/', views.Expense_File_Report.as_view(), name='expense_file_report'),
    path('invoice_file_report/', views.Invoice_File_Report.as_view(), name='invoice_file_report'),


    path('test-list/', views.Test_List.as_view(), name='test-list'),

        
]
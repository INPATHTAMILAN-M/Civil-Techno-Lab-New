from django.urls import path, include

from . import views
from .views import (
    QuotationCreateView,
    QuotationRetrieveView,
    QuotationListView,
    QuotationUpdateView,
    QuotationItemCreateView,
    QuotationItemListView,
    QuotationItemRetrieveView,
    QuotationItemUpdateView,
    QuotationItemDeleteView,
    QuotationReportList,
    QuotationReportCreate,
    InvoiceReportZipAPIView,
    QuotationReportDetail,
    QuotationReportUpdate,
    InvoiceReportListView,
    InvoiceReportGetView,
    CustomerDiscountViewSet
)

from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'customer-discount', CustomerDiscountViewSet, basename='customer-discount')

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

    # madhan
    path('pending_payment/', views.Pending_Payment.as_view(), name='pending payment'),

    # invoice file upload
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

    path('invoice-reports/zip/', InvoiceReportZipAPIView.as_view(), name='invoice_reports_zip'),

    path('quotations/', QuotationListView.as_view(), name='quotation-list'),          # List all quotations
    path('quotations/create/', QuotationCreateView.as_view(), name='quotation-create'), # Create a new quotation
    path('quotations/<int:pk>/', QuotationRetrieveView.as_view(), name='quotation-retrieve'), # Retrieve a single quotation
    path('quotations/<int:pk>/update/', QuotationUpdateView.as_view(), name='quotation-update'), # Update a quotation

    path('quotation-items/', QuotationItemListView.as_view(), name='quotation-item-list'),  # List all QuotationItems
    path('quotation-items/create/', QuotationItemCreateView.as_view(), name='quotation-item-create'),  # Create QuotationItem
    path('quotation-items/<int:pk>/', QuotationItemRetrieveView.as_view(), name='quotation-item-retrieve'),  # Retrieve QuotationItem
    path('quotation-items/<int:pk>/delete/', QuotationItemDeleteView.as_view(), name='quotation-item-delete'),
    path('quotation-items/<int:pk>/update/', QuotationItemUpdateView.as_view(), name='quotation-item-update'),  # Update QuotationItem

    path('quotation-reports/', QuotationReportList.as_view(), name='quotation-report-list'),
    path('quotation-reports/<int:pk>/', QuotationReportDetail.as_view(), name='quotation-report-detail'),

    path('invoice-reports/', InvoiceReportListView.as_view(), name='quotation-report-list'),
    path('invoice-reports/<int:pk>/', InvoiceReportGetView.as_view(), name='quotation-report-list'),

    # Include router URLs
    path('', include(router.urls)),
]

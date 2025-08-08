from django.urls import path, include

from account.viewset.employee import EmployeeViewSet
from general.viewsets.expence_viewset import ExpenseViewSet
from payment.viewsets.expense_entry import Expense_Entry_ViewSet
from payment.viewsets.invoice_file import InvoiceFileViewSet
from payment.viewsets.quotation import QuotationViewSet

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
    InvoiceReportZipAPIView,
    QuotationReportDetail,
    InvoiceReportListView,
    InvoiceReportGetView,
)
from .viewsets import (
    CustomerDiscountViewSet, 
    ReceiptViewSet, 
    TestViewSet,
    InvoiceTestViewSet,
    InvoiceViewSet,
    MaterialViewSet,
    InvoiceDiscountViewSet,
    InvoiceTaxViewSet,
    QuotationTaxViewSet

)
from account.viewset import (
    CityViewSet, StateViewSet, 
    CountryViewSet, CustomerViewSet,
    GenericHistoryViewSet
)
from general.viewsets.tax import TaxViewSet
from account.viewset import UserlogsViewSet

from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
from account.models import State, City, Country, Employee, Customer
from payment.models import (
    Quotation, QuotationItem, QuotationReport,
    Invoice, Invoice_Test, 
    Test_Report,Receipt,
    Expense_Entry,Invoice_File_Category,
    Invoice_File,SalesMode,InvoiceReport,
    CustomerDiscount,InvoiceDiscount
)
from general.models import Material,Test,Expense,Tax


router = DefaultRouter()

router.register(r'invoice-taxes', InvoiceTaxViewSet, basename='invoice-tax')
router.register(r'quotation-taxes', QuotationTaxViewSet, basename='quotation-tax')
router.register(r'customer-discount', CustomerDiscountViewSet, basename='customer-discount')
router.register(r'receipt', ReceiptViewSet, basename='receipt')
router.register(r'test', TestViewSet, basename='test')
router.register(r'invoice-test', InvoiceTestViewSet, basename='invoice-test')
router.register(r'invoice', InvoiceViewSet, basename='invoice')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'state', StateViewSet, basename='state')
router.register(r'city', CityViewSet, basename='city')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'material', MaterialViewSet, basename='material')
router.register(r'tax', TaxViewSet, basename='tax')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'expense', ExpenseViewSet, basename='expense')
router.register(r'quotation', QuotationViewSet, basename='quotation')
router.register(r'expense-entry', Expense_Entry_ViewSet, basename='expense-entry')
router.register(r'invoice-file', InvoiceFileViewSet, basename='invoice-file')
router.register(r'invoice-discount', InvoiceDiscountViewSet, basename='invoice-discount')
router.register(r'user-logs',UserlogsViewSet,basename='authlog')

# History Routers
router.register(r'country-history', GenericHistoryViewSet.as_viewset(Country), basename='country-history')
router.register(r'city-history', GenericHistoryViewSet.as_viewset(City), basename='city-history')
router.register(r'state-history', GenericHistoryViewSet.as_viewset(State), basename='state-history')
router.register(r'customer-history', GenericHistoryViewSet.as_viewset(Customer), basename='customer-history')
router.register(r'employee-history', GenericHistoryViewSet.as_viewset(Employee), basename='employee-history')
router.register(r'quotation-history', GenericHistoryViewSet.as_viewset(Quotation), basename='quotation-history')
router.register(r'quotation-report-history', GenericHistoryViewSet.as_viewset(QuotationReport), basename='quotation-report-history')
router.register(r'quotation-item-history', GenericHistoryViewSet.as_viewset(QuotationItem), basename='quotation-item-history')
router.register(r'invoice-history', GenericHistoryViewSet.as_viewset(Invoice), basename='invoice-history')
router.register(r'invoice-test-history', GenericHistoryViewSet.as_viewset(Invoice_Test), basename='invoice-test-history')
router.register(r'test-report-history', GenericHistoryViewSet.as_viewset(Test_Report), basename='test-report-history')
router.register(r'receipt-history', GenericHistoryViewSet.as_viewset(Receipt), basename='receipt-history')
router.register(r'expense-entry-history', GenericHistoryViewSet.as_viewset(Expense_Entry), basename='expense-entry-history')
router.register(r'invoice-file-category-history', GenericHistoryViewSet.as_viewset(Invoice_File_Category), basename='invoice-file-category-history')
router.register(r'invoice-file-history', GenericHistoryViewSet.as_viewset(Invoice_File), basename='invoice-file-history')
router.register(r'sales-mode', GenericHistoryViewSet.as_viewset(SalesMode), basename='sales-mode-history')
router.register(r'invoice-report-history', GenericHistoryViewSet.as_viewset(InvoiceReport), basename='invoice-report-history')
router.register(r'customer-discount-history', GenericHistoryViewSet.as_viewset(CustomerDiscount), basename='customer-discount-history')
router.register(r'invoice-discount-history', GenericHistoryViewSet.as_viewset(InvoiceDiscount), basename='invoice-discount-history') 
router.register(r'invoice-history', GenericHistoryViewSet.as_viewset(Invoice), basename='invoice-history')

router.register(r'material-history', GenericHistoryViewSet.as_viewset(Material), basename='material-history')
router.register(r'test-history', GenericHistoryViewSet.as_viewset(Test), basename='test-history')
router.register(r'expense-history', GenericHistoryViewSet.as_viewset(Expense), basename='expense-history')
router.register(r'tax-history', GenericHistoryViewSet.as_viewset(Tax), basename='tax-history')
router.register(r'user-history', GenericHistoryViewSet.as_viewset(User), basename='user-history')

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

    # # madhan
    # path('pending_payment/', views.Pending_Payment.as_view(), name='pending payment'),

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
    # path('test-list/', views.Test_List.as_view(), name='test-list'),



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

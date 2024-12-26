from django.contrib import admin
from django.urls import path

from general.views.tax_views import TaxEnableListView, TaxListView
from .import views1

urlpatterns = [

    path('create_tax/', views1.Manage_Tax.as_view(), name='create_tax'),
    # path('tax_list/',views1.Manage_Tax.as_view(), name='tax_list'),
    path('edit_tax/<int:id>/',views1.Manage_Tax.as_view(), name='edit_tax'),
    path('delete_tax/<int:id>/',views1.Manage_Tax.as_view(), name='delete_tax'),
    path('create_material/', views1.Manage_Material.as_view(), name='create_tax'),
    path('material_list/',views1.Manage_Material.as_view(), name='tax_list'),
    path('edit_material/<int:id>/',views1.Manage_Material.as_view(), name='edit_tax'),
    path('delete_material/<int:id>/',views1.Manage_Material.as_view(), name='delete_tax'),
    path('create_report_template/', views1.Create_Report_Template.as_view(), name='create_report_template'),
    path('report_template_list/', views1.List_Report_Template.as_view(), name='report_template_list'),
    path('edit_report_template/<int:id>/', views1.Edit_Report_Template.as_view(), name='edit_report_template'),
    path('delete_report_template/<int:id>/', views1.Delete_Report_Template.as_view(), name='delete_report_template'),
    path('create_test/', views1.Create_Test.as_view(), name='create_test'),
    path('test_list/',views1.List_Test.as_view(), name='test_list'),
    path('edit_test/<int:id>/', views1.Edit_Test.as_view(), name='edit_test'),
    path('delete_test/<int:id>/', views1.Delete_Test.as_view(), name='delete_test'),
    path('create_expense/', views1.Manage_Expense.as_view(), name='create_expense'),
    path('expense_list/', views1.Manage_Expense.as_view(), name='expense_list'),
    path('edit_expense/<int:id>/', views1.Manage_Expense.as_view(), name='edit_expense'),
    path('delete_expense/<int:id>/',views1.Manage_Expense.as_view(), name='delete_expense'),

    path('tax_list/', TaxListView.as_view(), name='tax-list'),
    path('enable_tax_list/', TaxEnableListView.as_view(), name='tax-list'),

]
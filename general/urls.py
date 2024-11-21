from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [

    path('create_tax/', views.Manage_Tax.as_view(), name='create_tax'),
    path('tax_list/',views.Manage_Tax.as_view(), name='tax_list'),
    path('edit_tax/<int:id>/',views.Manage_Tax.as_view(), name='edit_tax'),
    path('delete_tax/<int:id>/',views.Manage_Tax.as_view(), name='delete_tax'),
    path('create_material/', views.Manage_Material.as_view(), name='create_tax'),
    path('material_list/',views.Manage_Material.as_view(), name='tax_list'),
    path('edit_material/<int:id>/',views.Manage_Material.as_view(), name='edit_tax'),
    path('delete_material/<int:id>/',views.Manage_Material.as_view(), name='delete_tax'),
    path('create_report_template/', views.Create_Report_Template.as_view(), name='create_report_template'),
    path('report_template_list/', views.List_Report_Template.as_view(), name='report_template_list'),
    path('edit_report_template/<int:id>/', views.Edit_Report_Template.as_view(), name='edit_report_template'),
    path('delete_report_template/<int:id>/', views.Delete_Report_Template.as_view(), name='delete_report_template'),
    path('create_test/', views.Create_Test.as_view(), name='create_test'),
    path('test_list/',views.List_Test.as_view(), name='test_list'),
    path('edit_test/<int:id>/', views.Edit_Test.as_view(), name='edit_test'),
    path('delete_test/<int:id>/', views.Delete_Test.as_view(), name='delete_test'),
    path('create_expense/', views.Manage_Expense.as_view(), name='create_expense'),
    path('expense_list/', views.Manage_Expense.as_view(), name='expense_list'),
    path('edit_expense/<int:id>/', views.Manage_Expense.as_view(), name='edit_expense'),
    path('delete_expense/<int:id>/',views.Manage_Expense.as_view(), name='delete_expense'),
       
]
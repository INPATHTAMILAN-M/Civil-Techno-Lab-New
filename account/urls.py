from django.contrib import admin
from django.urls import path
from .import views



urlpatterns = [
    
    path('login/',views.Login_View.as_view(), name='api_login'),
    path('logout/',views.Logout.as_view(), name='api_logout'),
    path('create_customer/', views.Create_Customer.as_view(), name='create_customer'),
    path('customer_list/', views.Customer_List.as_view(), name='customer_list'),
    path('edit_customer/<int:id>/', views.Manage_Customer.as_view(), name='edit_customer'),
    path('delete_customer/<int:id>/', views.Manage_Customer.as_view(), name='delete_customer'),
    path('create_employee/', views.Manage_Employee.as_view(), name='create_employee'),
    path('employee_list/', views.Manage_Employee.as_view(), name='employee_list'),
    path('edit_employee/<int:id>/', views.Manage_Employee.as_view(), name='edit_employee'),
    path('delete_employee/<int:id>/', views.Manage_Employee.as_view(), name='delete_employee'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path("user-logs/", views.Userlogs.as_view(), name=""),
    
    path('create_city/', views.Manage_City.as_view(), name='create_city'),
    path('city_list/',views.Manage_City.as_view(), name='city_list'),
    path('edit_city/<int:id>/',views.Manage_City.as_view(), name='edit_city'),
    path('delete_city/<int:id>/',views.Manage_City.as_view(), name='delete_city'),

    
]


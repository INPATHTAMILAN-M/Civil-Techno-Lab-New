from django.contrib import admin
from .models import Customer,Employee, City, State, Country, UserActivity

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(UserActivity)

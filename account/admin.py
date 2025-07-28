from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Customer,Employee, City, State, Country, UserActivity

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(City)
admin.site.register(State,SimpleHistoryAdmin)
admin.site.register(Country)
admin.site.register(UserActivity)

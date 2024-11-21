from django.contrib import admin
from .models import Tax ,Material,Report_Template,Print_Format,Letter_Pad_Logo,Test,Expense
#from import_export.admin import ImportExportModelAdmin

admin.site.register(Tax)
admin.site.register(Material)
admin.site.register(Report_Template)
admin.site.register(Print_Format)
admin.site.register(Letter_Pad_Logo)
admin.site.register(Test)
admin.site.register(Expense)

from django.contrib import admin
from .models import (
    Expense_Entry,
    SalesMode,
    Invoice,
    Invoice_File,
    Invoice_Test,
    Invoice_File_Category,
    Receipt,
    Quotation,
    QuotationItem
)


class AInline(admin.TabularInline):
    model = Invoice_Test


class ReceiptInline(admin.TabularInline):
    model = Receipt


@admin.register(Invoice)
class Invoice_Admin(admin.ModelAdmin):
    inlines = [ReceiptInline, AInline]
    list_display = [
        'customer_name',
        'customer_gst_no',
        'invoice_no',
        'date',
        'amount',
        'cgst_tax',
        'sgst_tax',
        'total_amount',
        'cash',
        'cheque_neft',
        'tax_deduction',
        'advance',
        'balance'
    ]


@admin.register(Expense_Entry)
class Expense_Entry_Admin(admin.ModelAdmin):
    list_display = ['date']


@admin.register(Invoice_Test)
class Invoice_Test_Admin(admin.ModelAdmin):
    pass


admin.site.register(SalesMode)
admin.site.register(Invoice_File)
admin.site.register(Invoice_File_Category)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
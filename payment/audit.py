from auditlog.registry import auditlog
from payment.models import (
    Invoice, Invoice_Test, 
    Test_Report,Receipt,
    Expense_Entry,Invoice_File_Category,
    Invoice_File,SalesMode,InvoiceReport,
    CustomerDiscount,InvoiceDiscount,
    Quotation, QuotationItem, QuotationReport
)
for model in [
    Invoice, Invoice_Test, 
    Test_Report,Receipt,
    Expense_Entry,Invoice_File_Category,
    Invoice_File,SalesMode,InvoiceReport,
    CustomerDiscount,InvoiceDiscount,
    Quotation, QuotationItem, QuotationReport
]:
    auditlog.register(model)



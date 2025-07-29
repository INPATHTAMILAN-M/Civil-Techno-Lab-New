import os
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Sum
from payment.models import Invoice, InvoiceReport  # Adjust import paths as necessary
from django.conf import settings

def generate_invoice_report(invoice, request):

    tax_mapping = {
        'SGST': 'SGST',
        'CGST': 'CGST',
        'IGST': 'IGST'
    }
    
    tax_display = "+".join(f"{tax_mapping[tax.tax_name]} ({round(tax.tax_percentage)}%)" for tax in invoice.tax.all())

    context = {
        'invoice': invoice,
        'customer': invoice.customer,
        'invoice_items': invoice.invoice_tests.all(),
        "total_amount": invoice.before_tax_amount if invoice.before_tax_amount else 0,  
        "before_tax_amount": invoice.before_tax_amount or 0,
        "after_tax_amount": invoice.after_tax_amount or 0,
        "discount_amount": invoice.discount or 0,
        "discount": invoice.invoice_discounts.first().discount if invoice.invoice_discounts.first() else 0, 
        'tax': invoice.tax.all(),
        "tax_total": invoice.after_tax_amount - invoice.before_tax_amount ,
        "tax_display": tax_display,
        "settings": settings,
    }
    html_content = render_to_string('invoice.html', context)

    pdf_file = HTML(string=html_content).write_pdf()

    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'invoice_report')
    os.makedirs(pdf_dir, exist_ok=True)

    # Define the file path where the PDF will be saved
    file_path = os.path.join(pdf_dir, f"invoice_report_{invoice.id}.pdf")

    # Write the PDF content to the file
    with open(file_path, 'wb') as f:
        f.write(pdf_file)

    # Update or create the InvoiceReport model with the generated PDF file
    invoice_report, created = InvoiceReport.objects.update_or_create(
        invoice=invoice, 
        defaults={'invoice_file': f"invoice_report/invoice_report_{invoice.id}.pdf"}
    )
    invoice_report.created_by = request.user
    invoice_report.save()

    # Return the file path or URL if you need it for further processing
    return file_path
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "civiltech.settings")
django.setup()

from general.models import Tax
from payment.models import Invoice, InvoiceTax, Invoice_Test,InvoiceDiscount,CustomerDiscount
from django.contrib.auth import get_user_model

User = get_user_model()

# 1️⃣ Get the first 2 enabled taxes
# taxes = Tax.objects.filter(tax_status='E').order_by('id')[:2]

# 2️⃣ Select a default user (modify this to your case)
default_user = User.objects.first()

# 3️⃣ Loop through all invoices and create InvoiceTax entries
# for invoice in Invoice.objects.all():
#     for tax in taxes:
#         InvoiceTax.objects.create(
#             invoice=invoice,
#             tax_name=tax.tax_name,
#             tax_percentage=tax.tax_percentage,
#             tax_amount=(invoice.total_amount * tax.tax_percentage / 100),
#             created_by=default_user,
#             modified_by=default_user
#         )

# print("✅ InvoiceTax entries created for all invoices.")

# invoice_tests = Invoice_Test.objects.all()

# for invoice_test in invoice_tests:
#     invoice_test.primary_signature = invoice_test.signature
#     invoice_test.secondary_signature = invoice_test.signature
#     invoice_test.save()



# from django.db import transaction

# # Prefetch related customer discounts to avoid N+1 queries
# customer_discounts = {
#     cd.customer_id: cd
#     for cd in CustomerDiscount.objects.select_related('customer')
# }

# with transaction.atomic():
#     for invoice in Invoice.objects.select_related('customer'):
#         discount = customer_discounts.get(invoice.customer_id)
#         if discount:  # Only create if discount exists
#             InvoiceDiscount.objects.create(
#                 invoice=invoice,
#                 discount=discount.discount,
#                 created_by=discount.created_by,
#                 modified_by=discount.modified_by
#             )


# tax = Tax.objects.last()


# for invoice in Invoice.objects.all():
#     InvoiceTax.objects.create(
#         invoice=invoice,
#         tax_name=tax.tax_name,
#         tax_percentage=tax.tax_percentage,
#         tax_amount=(invoice.total_amount * tax.tax_percentage / 100),
#         created_by=default_user,
#         modified_by=default_user,
#         enabled = False
#     )

# import qrcode
# import os
# from django.conf import settings
# from django.utils import timezone
# from payment.models import Invoice  # adjust the import path to your app


# def get_financial_year():
#     now = timezone.now()
#     year = now.year
#     month = now.month
#     if month >= 4:
#         fy_start = year
#         fy_end = year + 1
#     else:
#         fy_start = year - 1
#         fy_end = year
#     return f"{str(fy_start)[2:]}-{str(fy_end)[2:]}"


# def generate_invoice_qrcodes():
#     financial_year = get_financial_year()

#     # Find the last invoice number for the year
#     last_invoice = Invoice.objects.filter(
#         invoice_no__endswith=f"/{financial_year}",
#         invoice_no__isnull=False
#     ).last()

#     last_invoice_no = 0
#     if last_invoice:
#         try:
#             last_invoice_no = int(last_invoice.invoice_no.split('/')[0])
#         except (ValueError, IndexError):
#             pass

#     # Get the invoices you want to generate QR codes for
#     invoice_list = Invoice.objects.all().order_by('-created_date')[:10]

#     counter = 0
#     for inv in invoice_list:
#         counter += 1
#         current_prefix = f"{(last_invoice_no + counter):03d}"

#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(f"{settings.QR_DOMAIN}/invoice/viewinvoicereport?id={inv.id}")
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         invoice_img_dir = "media/invoice"
#         os.makedirs(invoice_img_dir, exist_ok=True)

#         invoice_img_filename = f"invoice_{current_prefix}-{financial_year}.png"
#         invoice_img_path = os.path.join(invoice_img_dir, invoice_img_filename)

#         img.save(invoice_img_path)

#         # Save relative path so MEDIA_URL works in templates
#         inv.invoice_image = f"media/invoice/{invoice_img_filename}"
#         inv.save()

#         print(f"QR code generated for invoice {inv.id}: {inv.invoice_image}")


# # Run the function
# generate_invoice_qrcodes()


# # QR code generation

# invoice_ids = list(Invoice.objects.order_by('-created_date')
#                    .values_list('id', flat=True)[:10])

# invoice_tests = Invoice_Test.objects.filter(invoice_id__in=invoice_ids)


# for test in invoice_tests:

#     qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=10,
#     border=4,
#     )
#     qr_url = f"{settings.QR_DOMAIN}/invoice/viewtestreport?id={test.id}"
#     qr.add_data(qr_url)
#     qr.make(fit=True)
#     qr_img = qr.make_image(fill_color="black", back_color="white")

#     qr_dir = os.path.join(settings.MEDIA_ROOT, "invoice_test")
#     os.makedirs(qr_dir, exist_ok=True)
#     qr_filename = f"invoice_{test.id}.png"
#     qr_path = os.path.join(qr_dir, qr_filename)
#     qr_img.save(qr_path)

#     qr_relative = f"media/invoice_test/{qr_filename}"
#     test.invoice_image = qr_relative
#     test.save()
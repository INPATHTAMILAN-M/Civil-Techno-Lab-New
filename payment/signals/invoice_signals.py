import logging
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from decimal import Decimal
from payment.models import Invoice, Invoice_Test, InvoiceDiscount, Receipt
from account.models import Customer

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Invoice.tax.through)
def update_invoice_on_tax_change(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        apply_invoice_calculation(instance)


@receiver([post_save, post_delete], sender=Invoice_Test)
@receiver([post_save, post_delete], sender=Receipt)
@receiver([post_save, post_delete], sender=InvoiceDiscount)
def update_invoice_totals(sender, instance, **kwargs):
    logger.info(f"[Signal Triggered] Sender: {sender.__name__}, Instance: {instance}")

    invoice = None

    if isinstance(instance, Invoice_Test):
        invoice = instance.invoice
        logger.info(f"Updating totals due to Invoice_Test (ID: {instance.id}) for Invoice (ID: {invoice.id if invoice else 'None'})")

    elif isinstance(instance, Receipt):
        invoice = instance.invoice_no
        logger.info(f"Updating totals due to Receipt (ID: {instance.id}) for Invoice (ID: {invoice.id if invoice else 'None'})")

    elif isinstance(instance, InvoiceDiscount):
        invoice = instance.invoice
        logger.info(f"Updating totals due to InvoiceDiscount (ID: {instance.id}) for Invoice (ID: {invoice.id if invoice else 'None'})")

    if invoice:
        apply_invoice_calculation(invoice)


def apply_invoice_calculation(invoice: Invoice):
    logger.info(f"Applying invoice calculations for Invoice ID: {invoice.id}")

    # 1. Base amount from tests
    invoice_tests = invoice.invoice_tests.all()
    total_amount = sum(it.quantity * it.price_per_sample for it in invoice_tests)

    # 2. Calculate discount from all related InvoiceDiscounts
    discount_percent_total = sum(d.discount for d in invoice.invoice_discounts.all())
    discount_amount = (Decimal(discount_percent_total) / Decimal('100')) * total_amount

    # 3. Calculate tax on original amount
    tax_total = 0
    if invoice.tax.exists():
        for tax in invoice.tax.all():
            tax_total += (tax.tax_percentage / 100) * total_amount

    # 4. Receipts
    receipts = Receipt.objects.filter(invoice_no=invoice)
    paid_amount = sum(r.amount for r in receipts)

    # 5. Final amounts
    balance = total_amount + tax_total - discount_amount - paid_amount
    before_tax_amount = total_amount - discount_amount
    after_tax_amount = total_amount - discount_amount + tax_total

    logger.info({
        "invoice_id": invoice.id,
        "total_amount": float(total_amount),
        "discount_applied": float(discount_amount),
        "tax_total": float(tax_total),
        "paid_amount": float(paid_amount),
        "final_balance": float(balance)
    })

    # 6. Update invoice
    invoice.before_tax_amount = before_tax_amount
    invoice.after_tax_amount = after_tax_amount
    invoice.total_amount = total_amount
    invoice.discount = discount_amount
    invoice.balance = balance
    invoice.advance = paid_amount
    invoice.save()
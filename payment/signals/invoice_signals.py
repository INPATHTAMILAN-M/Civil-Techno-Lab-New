import logging
from decimal import Decimal
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from payment.models import Invoice, Invoice_Test, InvoiceDiscount, Receipt

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
    elif isinstance(instance, Receipt):
        invoice = instance.invoice_no
    elif isinstance(instance, InvoiceDiscount):
        invoice = instance.invoice

    if invoice:
        apply_invoice_calculation(invoice)


def apply_invoice_calculation(invoice: Invoice):
    logger.info(f"Applying invoice calculations for Invoice ID: {invoice.id}")

    # 1. Base amount from tests
    invoice_tests = invoice.invoice_tests.all()
    total_amount = sum(it.quantity * it.price_per_sample for it in invoice_tests)

    # 2. Calculate discount
    discount_percent_total = sum(d.discount for d in invoice.invoice_discounts.all())
    discount_amount = (Decimal(discount_percent_total) / Decimal('100')) * total_amount

    # 3. Tax
    tax_total = sum(
        (tax.tax_percentage / 100) * (total_amount - discount_amount)
        for tax in invoice.tax.all()
    )

    # 4. Receipts
    receipts = Receipt.objects.filter(invoice_no=invoice)
    paid_amount = sum(r.amount for r in receipts)

    # 5. Final calculations
    before_tax_amount = total_amount - discount_amount
    after_tax_amount = before_tax_amount + tax_total
    balance = after_tax_amount - paid_amount

    updated_fields = []

    def check_and_update(field, new_value):
        old_value = getattr(invoice, field)
        if old_value != new_value:
            setattr(invoice, field, new_value)
            updated_fields.append(field)

    check_and_update("before_tax_amount", before_tax_amount)
    check_and_update("after_tax_amount", after_tax_amount)
    check_and_update("total_amount", total_amount)
    check_and_update("discount", discount_amount)
    check_and_update("balance", balance)
    check_and_update("advance", paid_amount)

    if updated_fields:
        invoice.save(update_fields=updated_fields)
        logger.info(f"Updated Invoice {invoice.id}: fields changed: {updated_fields}")
    else:
        logger.info(f"No actual field changes for Invoice ID: {invoice.id}, skipped save.")


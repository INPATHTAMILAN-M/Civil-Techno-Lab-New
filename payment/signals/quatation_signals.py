from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Quotation, QuotationItem


@receiver(post_save, sender=QuotationItem)
@receiver(post_delete, sender=QuotationItem)
def update_quotation_total(sender, instance, **kwargs):
    quotation = instance.quotation
    tax = quotation.tax.all()
    subtotal = sum(item.total_price() for item in quotation.quotation_items.all())
    # tax_amount = sum(t.calculate_tax(subtotal) for t in tax)
    # quotation.total_amount = subtotal + tax_amount
    quotation.total_amount = subtotal
    quotation.save()
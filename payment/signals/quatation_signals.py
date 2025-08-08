from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Quotation, QuotationItem, QuotationTax


def calculate_total_amount(quotation):
    """
    Compute subtotal, tax, and total values.
    """
    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    taxes = quotation.quotation_taxes.filter(enabled=True)

    sub_total = sum(item.total_price() for item in quotation_items)
    tax_amount = sum(
        (t.tax_percentage / 100) * sub_total
        for t in taxes
    )

    before_tax = sub_total
    after_tax = sub_total + tax_amount
    total = after_tax

    return total, sub_total, before_tax, after_tax


def update_quotation_totals(quotation):
    """
    Centralized quotation update.
    """
    total, sub_total, before_tax, after_tax = calculate_total_amount(quotation)

    updated_fields = []
    if quotation.total_amount != total:
        quotation.total_amount = total
        updated_fields.append("total_amount")
    if quotation.sub_total != sub_total:
        quotation.sub_total = sub_total
        updated_fields.append("sub_total")
    if quotation.before_tax != before_tax:
        quotation.before_tax = before_tax
        updated_fields.append("before_tax")
    if quotation.after_tax != after_tax:
        quotation.after_tax = after_tax
        updated_fields.append("after_tax")

    if updated_fields:
        quotation.save(update_fields=updated_fields)


@receiver([post_save, post_delete], sender=QuotationItem)
@receiver([post_save, post_delete], sender=QuotationTax)
def quotation_related_changed(sender, instance, **kwargs):
    """
    Triggered when QuotationItem or QuotationTax is added/updated/deleted.
    """
    if instance.quotation:
        update_quotation_totals(instance.quotation)


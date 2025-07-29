from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils.timezone import now
from ..models import Quotation, QuotationItem


def calculate_total_amount(quotation):
    """
    Compute subtotal, tax, and total values.
    """
    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    tax_set = quotation.tax.all()

    sub_total = sum(item.total_price() for item in quotation_items)
    tax_amount = sum(t.calculate_tax(sub_total) for t in tax_set)

    before_tax = sub_total
    after_tax = sub_total + tax_amount
    total = after_tax

    return total, sub_total, before_tax, after_tax


def update_quotation_totals(quotation):
    """
    Centralized quotation update.
    """
    total, sub_total, before_tax, after_tax = calculate_total_amount(quotation)

    # Only save if values have actually changed
    if (
        quotation.total_amount != int(total)
        or quotation.sub_total != int(sub_total)
        or quotation.before_tax != before_tax
        or quotation.after_tax != after_tax
    ):
        quotation.total_amount = int(total)
        quotation.sub_total = int(sub_total)
        quotation.before_tax = before_tax
        quotation.after_tax = after_tax
        quotation.save(update_fields=["total_amount", "sub_total", "before_tax", "after_tax"])


@receiver([post_save, post_delete], sender=QuotationItem)
def quotation_item_changed(sender, instance, **kwargs):
    """
    Triggered when QuotationItem is added/updated/deleted.
    """
    if instance.quotation:
        update_quotation_totals(instance.quotation)


@receiver(m2m_changed, sender=Quotation.tax.through)
def quotation_tax_changed(sender, instance, action, **kwargs):
    """
    Triggered when tax M2M field is changed.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        update_quotation_totals(instance)


@receiver(post_save, sender=Quotation)
def handle_quotation_save(sender, instance, created, **kwargs):
    """
    Handle initial quotation number and totals only on creation.
    """
    if created and not instance.quotation_number:
        current_date = now()
        year = (
            f"{current_date.year - 1}-{str(current_date.year)[2:]}"
            if current_date.month < 4
            else f"{current_date.year}-{str(current_date.year + 1)[2:]}"
        )
        start_date = f"{current_date.year - 1}-04-01" if current_date.month < 4 else f"{current_date.year}-04-01"
        count = Quotation.objects.filter(date_created__gte=start_date).count()

        instance.quotation_number = instance.QUOTATION_FORMAT.format(number=count + 1, year=year)
        update_quotation_totals(instance)
        instance.save(update_fields=["quotation_number", "total_amount", "sub_total", "before_tax", "after_tax"])

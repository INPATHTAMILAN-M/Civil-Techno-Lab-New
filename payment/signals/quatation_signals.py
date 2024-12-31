from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from weasyprint import HTML
import os

from ..models import Quotation, QuotationItem, QuotationReport


def calculate_total_amount(quotation):

    if not quotation.pk:
        quotation.save()

    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    tax = quotation.tax.all()

     
    
    sub_total = sum(item.total_price() for item in quotation_items)
    tax_amount = sum(t.calculate_tax(sub_total) for t in tax)

    for q in quotation_items:
        print(f"{q.price_per_sample} ** {q.quantity}")
    print("Subtotal:", sub_total)
    print("Tax Amount:", tax_amount)
    return sub_total + tax_amount , sub_total

@receiver([post_save,pre_save,post_delete], sender=QuotationItem)
def update_quotation_total(sender, instance, **kwargs):
    print("QuotationItem updated....................................")
    if instance:
        new_total, sub_total = calculate_total_amount(instance.quotation)
        instance.quotation.total_amount = int(new_total)
        instance.quotation.sub_total = int(sub_total)
        instance.quotation.save()
        print("Quotation total amount updated:", new_total)
    else:
        print("Quotation not set for QuotationItem")


@receiver([post_save,post_delete], sender=Quotation)
def update_quotation_total(sender, instance, created=False, **kwargs):
    print("QuotationItem updated....................................")

    if instance and not getattr(instance, '_updating_total', False):
        try:
            instance._updating_total = True
            new_total, sub_total = calculate_total_amount(instance)
            instance.total_amount = int(new_total)
            instance.sub_total = int(sub_total)
            instance.save()
            print("Quotation total amount updated:", new_total)
        finally:
            instance._updating_total = False
    else:
        print("Quotation not set for QuotationItem")

@receiver([pre_save, post_save, m2m_changed], sender=Quotation.tax.through)
def handle_quotation_save(sender, instance, **kwargs):
    if not instance.pk:  # For new instances
        instance.total_amount = 0
        instance.save()
    else:
        new_total, sub_total = calculate_total_amount(instance)
        instance.total_amount=int(new_total)
        instance.sub_total=int(sub_total)
        instance.save()
        print("Pre-save: Quotation total amount updated:", new_total)




from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.dispatch import receiver
import os
from django.utils.timezone import now



from ..models import Quotation, QuotationItem, QuotationReport


def calculate_total_amount(quotation):

    if not quotation.pk:
        quotation.save()

    quotation_items = QuotationItem.objects.filter(quotation=quotation)
    tax = quotation.tax.all()
    
    sub_total = sum(item.total_price() for item in quotation_items)
    tax_amount = sum(t.calculate_tax(sub_total) for t in tax)

    before_tax_amount = sub_total 
    after_tax_amount = sub_total + tax_amount

    for q in quotation_items:
        print(f"{q.price_per_sample} ** {q.quantity}")
    print("Subtotal:", sub_total)
    print("Tax Amount:", tax_amount)
    return sub_total + tax_amount , sub_total, before_tax_amount,after_tax_amount


@receiver([post_save, post_delete], sender=QuotationItem)
def update_quotation_totals(sender, instance, **kwargs):
    """
    Recalculate totals for a Quotation whenever a QuotationItem is added, updated, or removed.
    """
    quotation = instance.quotation
    if quotation:
        try:
            # Calculate totals
            new_total, sub_total, before_tax, after_tax = calculate_total_amount(quotation)

            # Update the Quotation
            quotation.total_amount = new_total
            quotation.sub_total = sub_total
            quotation.before_tax = before_tax
            quotation.after_tax = after_tax
            quotation.save()
            print(f"Quotation {quotation.id} totals updated: Total - {new_total}, Subtotal - {sub_total}")
        except Exception as e:
            print(f"Error updating quotation totals: {e}")



@receiver([post_save, post_delete], sender=Quotation)
def update_quotation_total(sender, instance, created=False, **kwargs):
    print("QuotationItem updated....................................")
    
    if instance and not getattr(instance, '_updating_total', False):
        try:
            instance._updating_total = True
            
            # Handle quotation number generation for new instances
            if created and not instance.quotation_number:
                current_date = now()
                year = (
                    f"{current_date.year-1}-{str(current_date.year)[2:]}"
                    if current_date.month < 4
                    else f"{current_date.year}-{str(current_date.year + 1)[2:]}"
                )
                start_date = f"{current_date.year-1}-04-01" if current_date.month < 4 else f"{current_date.year}-04-01"
                count = Quotation.objects.filter(date_created__gte=start_date).count()
                instance.quotation_number = instance.QUOTATION_FORMAT.format(number=count + 1, year=year)
            
            # Calculate and update totals
            new_total, sub_total, before_tax, after_tax = calculate_total_amount(instance)
            instance.total_amount = int(new_total)
            instance.sub_total = int(sub_total)
            instance.before_tax = before_tax
            instance.after_tax = after_tax
            
            # Save all changes at once
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
        new_total, sub_total, before_tax, after_tax = calculate_total_amount(instance)
        instance.total_amount=int(new_total)
        instance.before_tax = before_tax
        instance.after_tax = after_tax
        instance.sub_total=int(sub_total)
        instance.save()




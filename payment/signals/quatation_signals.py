from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from payment.models import QuotationItem

@receiver(post_save, sender=QuotationItem)
def update_quotation_total_on_save(sender, instance, **kwargs):
    instance.quotation.recalculate_total()

@receiver(post_delete, sender=QuotationItem)
def update_quotation_total_on_delete(sender, instance, **kwargs):
    instance.quotation.recalculate_total()
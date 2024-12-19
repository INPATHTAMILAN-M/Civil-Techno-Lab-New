from django.db import models
from django.utils.timezone import now

class Quotation(models.Model):
    QUOTATION_FORMAT = "QUO-{number}/{year}"
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="quotations")
    quotation_number = models.CharField(max_length=20, unique=True, blank=True)  # Will be auto-generated
    date_created = models.DateField(default=now)
    tax = models.ManyToManyField('general.Tax', blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.quotation_number:
            current_date = now()
            year = (
                f"{current_date.year-1}-{str(current_date.year)[2:]}"
                if current_date.month < 4
                else f"{current_date.year}-{str(current_date.year + 1)[2:]}"
            )
            start_date = f"{current_date.year-1}-04-01" if current_date.month < 4 else f"{current_date.year}-04-01"
            count = Quotation.objects.filter(date_created__gte=start_date).count() + 1
            self.quotation_number = self.QUOTATION_FORMAT.format(number=count, year=year)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.quotation_number

    def items(self):
        return self.quotation_items.all()

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="quotation_items")
    test = models.ForeignKey('general.Test', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    quotation_image = models.CharField(max_length=255, null=True, blank=True)
    signature = models.ForeignKey('account.Employee', on_delete=models.CASCADE, null=True, blank=True)
    is_authorised_signatory = models.BooleanField(default=False)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, related_name='quotation_items_created')
    created_date = models.DateField(auto_now_add=True, null=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, related_name='quotation_items_modified')
    modified_date = models.DateTimeField(auto_now=True, null=True)

    def total_price(self):
        return self.quantity * self.test.price_per_piece

    def __str__(self):
        return f"{self.test.test_name} - {self.quotation.quotation_number}"


class QuotationReport(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="quotation_reports")
    report = models.FileField(upload_to='reports/')
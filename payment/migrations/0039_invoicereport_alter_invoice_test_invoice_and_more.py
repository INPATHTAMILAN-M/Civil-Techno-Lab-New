# Generated by Django 4.2.7 on 2024-12-21 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0038_remove_quotationitem_is_authorised_signatory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_file', models.FileField(upload_to='invoice_reports/')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_reports_created', to=settings.AUTH_USER_MODEL)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.invoice')),
            ],
        ),
        migrations.AlterField(
            model_name='invoice_test',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_tests', to='payment.invoice'),
        ),
        migrations.AlterField(
            model_name='quotationitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Invoice_Report',
        ),
    ]

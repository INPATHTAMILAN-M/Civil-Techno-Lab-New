# Generated by Django 4.2.7 on 2024-01-04 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_delete_expense_user'),
        ('payment', '0005_invoice_place_of_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='tax',
        ),
        migrations.AddField(
            model_name='invoice',
            name='tax',
            field=models.ManyToManyField(to='general.tax'),
        ),
    ]

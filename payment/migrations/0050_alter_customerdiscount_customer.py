# Generated by Django 4.2.7 on 2025-04-26 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_employee_is_active'),
        ('payment', '0049_alter_customerdiscount_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdiscount',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_discount', to='account.customer'),
        ),
    ]

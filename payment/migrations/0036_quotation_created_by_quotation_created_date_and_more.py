# Generated by Django 4.2.7 on 2024-12-20 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0035_remove_quotationitem_quotation_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotation',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotation',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
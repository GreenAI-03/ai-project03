# Generated by Django 5.0.7 on 2024-08-14 22:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_system', '0005_customer_rename_product_sale_product_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='e_invoice_carrier',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='special_requests',
            field=models.TextField(blank=True, null=True),
        ),
    ]

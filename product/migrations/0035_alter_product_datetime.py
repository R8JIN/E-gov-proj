# Generated by Django 3.2.3 on 2023-07-18 17:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_alter_product_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 18, 23, 15, 16, 778771), null=True),
        ),
    ]
# Generated by Django 4.2.1 on 2023-07-13 06:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_product_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 13, 12, 34, 41, 746314), null=True),
        ),
    ]

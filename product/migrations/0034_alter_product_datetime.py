# Generated by Django 3.2.3 on 2023-07-18 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_auto_20230718_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 18, 22, 40, 46, 405660), null=True),
        ),
    ]

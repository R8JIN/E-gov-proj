# Generated by Django 4.2.1 on 2023-07-12 13:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bidding', '0011_alter_bid_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 12, 19, 9, 35, 645516), null=True),
        ),
    ]
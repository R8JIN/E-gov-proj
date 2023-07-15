# Generated by Django 4.1.7 on 2023-07-14 13:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bidding', '0028_alter_bid_datetime_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 14, 18, 57, 34, 64075)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 7, 14, 18, 57, 34, 65072)),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 14, 18, 57, 34, 64075)),
        ),
    ]
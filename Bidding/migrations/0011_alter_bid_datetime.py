# Generated by Django 4.2.1 on 2023-07-12 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bidding', '0010_alter_bid_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

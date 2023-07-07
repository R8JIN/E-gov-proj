from django.db import models
from product.models import Product
from Account.models import User
from datetime import datetime
# Create your models here.


class WatchList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now, blank=True)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid_amt = models.FloatField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    # class META:
    #     def verbose_name(self):
    #         return

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    price = models.FloatField()
    date = models.DateField(default=datetime.now, blank=True)
    status = models.CharField(max_length=255,
                              choices=[
                                ('Requested', 'Requested'),
                                ('Dispatched', 'Dispatched'),
                                ('Delivered', 'Delivered'),
                                ('Cancelled', 'Cancelled'),
                                       ], default='Requested')


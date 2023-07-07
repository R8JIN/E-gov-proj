from django.db import models
from countdowntimer_model.models import CountdownTimer
from datetime import datetime
from Account.models import User
# Create your models here.


class Category(models.Model, ):
    title = models.CharField(max_length=255)
    Description = models.TextField()

    def __str__(self):
        return self.title


class Product(CountdownTimer, models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    thumbNails = models.ImageField()
    images = models.FileField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)
    final_price = models.FloatField(null=True, blank=True)

    def __str__(self):
       return self.title


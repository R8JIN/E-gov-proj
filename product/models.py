from django.db import models
from countdowntimer_model.models import CountdownTimer
from datetime import datetime
from Account.models import User, Payment

# Create your models here.


class Category(models.Model, ):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/category/{self.id}/'


class Product(CountdownTimer, models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    thumbNails = models.ImageField()
    images = models.FileField(null=True, blank=True)
    final_price = models.FloatField(null=True,blank=True)
    engine_number = models.CharField(max_length=255,null=True, blank=True)
    chassis_number = models.CharField(max_length=255,null=True, blank=True)
    datetime = models.DateTimeField(default=datetime.now(), null=True, blank=True)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)

    def __str__(self):
       return self.title

    def get_absolute_url(self):
       return f'/category/{self.category.id}/{self.id}/'

    def get_image(self):
            if self.thumbNails:
                return 'http://localhost:8000' + self.thumbNails.url
            return ''


from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False, blank=True,null=True)


class PaymentMethod(models.Model):
    payment_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.payment_type


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=255, null=True)





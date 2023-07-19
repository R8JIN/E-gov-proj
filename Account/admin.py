from django.contrib import admin
from .models import User, Payment, PaymentMethod

admin.site.register(User)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
# Register your models here.

from django.db import models
from decimal import Decimal

class Subscribers(models.Model):
    emailId = models.CharField(max_length=120, default='', db_index=True)
    location = models.CharField(max_length=200, default='')
    latitude = models.DecimalField(max_digits=11,decimal_places=4, default=Decimal('0.0000'))
    longitude = models.DecimalField(max_digits=11,decimal_places=4, default=Decimal('0.0000'))
    created_date = models.DateTimeField(auto_now=True)
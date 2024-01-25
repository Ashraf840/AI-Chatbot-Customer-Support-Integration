from django.db import models

# Create your models here.
# models.py in your Django app
from django.db import models

class TaDaRateSheet(models.Model):
    grade = models.IntegerField()
    daily_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as needed

from django.db import models


# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50)

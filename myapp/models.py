from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Amount = models.FloatField()  # Field for the amount of the transaction
    CategoryID = models.ForeignKey('Category', on_delete=models.CASCADE)   # Field for the category ID of the transaction
    Description = models.CharField(max_length=255)  # Field for the description of the transaction
    TransactionDate = models.DateTimeField()  # Field for the date of the transaction
    TransactionType = models.CharField(max_length=50)  # Field for the type of the transaction (e.g., 'credit', 'debit')

    def __str__(self):
        return self.Description


class Category(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)  # Field for the amount of the transaction
    Description = models.CharField(max_length=255)  # Field for the description of the transaction
    TransactionDate = models.DateTimeField()  # Field for the date of the transaction



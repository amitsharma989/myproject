from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    def __str__(self):
        return self.name
    

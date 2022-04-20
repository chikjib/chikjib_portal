from tabnanny import verbose
from django.db.models.deletion import CASCADE
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Datashare Categories"
    
class ProductList(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    product_code = models.CharField(max_length=255)
    quantity = models.IntegerField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Mtn Datashare Product List"
    
class AirtelProductList(models.Model):
    product_code = models.CharField(max_length=255)
    quantity = models.IntegerField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Airtel Datashare Product List"
from django.db import models

class Education(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Education Product List"
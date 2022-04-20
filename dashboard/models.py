from tabnanny import verbose
from unicodedata import digit
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
import requests
from django.conf import settings


class PortalWebhookMessage(models.Model):
    received_at = models.DateTimeField(help_text="When we received the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]

class PaymentNotification(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    deposit_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    description = models.TextField()
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Recent Payment List"
    
class ServiceNotification(models.Model):
    notification = models.CharField(max_length=255)
    
    def __str__(self):
        return self.notification
    
    class Meta:
        verbose_name_plural = "Service Status Notification"
    

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    transaction_ref = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    service = models.CharField(max_length=255,blank=True, null=True)
    destination = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_ref
    

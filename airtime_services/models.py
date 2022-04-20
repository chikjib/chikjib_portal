from django.db import models
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    wallet_balance = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    wallet_in = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    wallet_out = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    phone_no = models.CharField(max_length=16,blank=True, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    state = models.CharField(max_length=100,blank=True, null=True)
    funding_account_no = models.CharField(max_length=255,blank=True, null=True)
    funding_bank = models.CharField(max_length=255,blank=True, null=True)
    tx_ref = models.CharField(max_length=255,blank=True, null=True) 
    order_ref = models.CharField(max_length=255,blank=True, null=True) 
    
    def save(self,*args, **kwargs):
        return super(Profile,self).save(*args, **kwargs)
        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
        

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username  

from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Profile
from dashboard.models import PaymentNotification, ServiceNotification, Transaction


def topup_wallet(modeladmin, request, queryset):
    for query in queryset:
        new_wallet_balance = query.user.profile.wallet_balance + query.amount
        Profile.objects.filter(user=query.user).update(wallet_balance=new_wallet_balance)
topup_wallet.short_description = 'Topup wallet for selected user'

class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = ('user','name','email','deposit_type','get_amount','description')
    actions = [topup_wallet,]
    
    def get_amount(self,instance):
        return "N" + str(instance.amount)
    get_amount.short_description = "Amount"
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
class ServiceNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification',)

    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','transaction_ref','type','service','destination','description','get_amount','created_at')
   
    
    def get_amount(self,instance):
        return "N" + str(instance.amount)
    get_amount.short_description = "Amount"
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    
admin.site.register(PaymentNotification,PaymentNotificationAdmin)
admin.site.register(ServiceNotification,ServiceNotificationAdmin)
admin.site.register(Transaction,TransactionAdmin)

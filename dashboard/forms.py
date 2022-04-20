from django import forms

from dashboard.models import PaymentNotification

class PaymentNofiticationForm(forms.ModelForm):
    class Meta:
        model = PaymentNotification
        fields = ('user', 'name','email','deposit_type','amount','description')

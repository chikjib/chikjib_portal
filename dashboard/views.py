from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.utils.crypto import get_random_string
from dashboard.models import Transaction
from django.contrib.auth.models import User
from django.db.transaction import atomic, non_atomic_requests
from secrets import compare_digest
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime as dt
import json
from django.utils import timezone
from dashboard.forms import PaymentNofiticationForm
from dashboard.models import PortalWebhookMessage, ServiceNotification


# Create your views here.
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'backend/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = Transaction.objects.filter(user=self.request.user).count()
        context["notifications"] = ServiceNotification.objects.all().order_by("-id").first()

        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD

        balance = requests.get('https://mobileairtimeng.com/httpapi/balance?userid='+api_user_id+'&pass='+api_password+'&jsn=json')
        response = balance.json()
        
        if response['code'] == 100:
            context['site_balance'] = response['message']
        
        
        return context

class TransactionView(LoginRequiredMixin,ListView):
    template_name = "backend/transactions.html"
    model = Transaction
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = Transaction.objects.filter(user=self.request.user)
        context["page_title"] = "Transactions"
        return context
    
class SupportView(LoginRequiredMixin,TemplateView):
    template_name = "backend/support.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Support"
        return context
    
    
@login_required
def FundView(request):
    if request.method == "POST":
        tx_ref = get_random_string(length=8)
        email = request.user.email
        phone_no = request.user.profile.phone_no
        firstname = request.user.first_name
        lastname = request.user.last_name
        narration = request.user.get_full_name()
        bvn = request.POST.get("bvn")
        
        url = 'https://api.flutterwave.com/v3/virtual-account-numbers'
        my_headers = {
            'Authorization' : 'Bearer '+settings.FLW_SECRET_KEY,
            # 'Content-Type': 'application/json',
        }
        data_obj = {
            # 'status':'inactive'
            'email': email,
            "is_permanent": True,
            "bvn":bvn,
            "tx_ref": tx_ref,
            "phonenumber": phone_no,
            "firstname": firstname,
            "lastname": lastname,
            "narration": narration   
        }
        
        # print(data_obj)
        user = User.objects.filter(email=request.user.email).first()
        if user.profile.funding_account_no is None and user.profile.funding_bank is None:
            result = requests.post(url,headers=my_headers,data=data_obj)
            result = result.json()
            print(result)
            if result['status'] == "success":
                account_no = result['data']['account_number']
                bank = result['data']['bank_name']
                user.profile.funding_account_no = account_no
                user.profile.funding_bank = bank
                user.profile.tx_ref = tx_ref
                user.profile.order_ref = result['data']['order_ref']
                user.save()
                
                # print(result.json())
                return redirect(reverse_lazy('fund_wallet'))
            
    page_title = "Fund Wallet" 
    context = {
        "page_title":page_title
    }
    return render(request,'backend/fund_wallet.html',context)

@csrf_exempt
@require_POST
@non_atomic_requests
def portal_webhook(request):
    given_token = request.headers.get("verif-hash", "")
    if not compare_digest(given_token, settings.PORTAL_WEBHOOK_TOKEN):
        return HttpResponseForbidden(
            "Incorrect token in Portal-Webhook-Token header.",
            content_type="text/plain",
        )

    PortalWebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=7)
    ).delete()
    payload = json.loads(request.body)
    PortalWebhookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    process_webhook_payload(payload)
    return HttpResponse("Message received okay.", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    # TODO: business logic
    print(payload)
    
# def getFunds(request):
#     return render(request)
#     # tx_ref = request.user.profile.tx_ref
#     # url = 'https://api.flutterwave.com/v3/transactions/'+tx_ref+'/verify'
#     # # print(url)
#     # my_headers = {
#     #     'Authorization' : 'Bearer '+settings.FLW_SECRET_KEY,
#     # }
#     # result = requests.get(url,headers=my_headers)
#     # print(result.json())
    
    
    
@login_required   
def PaymentNotificationView(request):
    if request.method == "POST":
        form = PaymentNofiticationForm(request.POST,initial={'user': request.user, 'name':request.user.get_full_name,'email':request.user.email})
        if form.is_valid():
            form.save()
            messages.success(request,"Payment Notification submitted successfully")
            return redirect('payment_notification')
        else:
            messages.warning(request,"An error occurred!")
            return redirect('payment_notification')
        
    form = PaymentNofiticationForm(initial={'user':request.user, 'name':request.user.get_full_name,'email':request.user.email})
    
    page_title = "Payment Notification" 
    
    context = {
        "form":form,
        "page_title":page_title
    }    
    return render(request,"backend/payment_notification.html",context)
    
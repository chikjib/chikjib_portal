from decimal import Decimal
from dashboard.models import Transaction
from django.core.mail import send_mail


# Registered users only
def CheckBalance(user,amount):
    if user.profile.wallet_balance < float(amount):
        return True
    else:
        return False
        
def TakeRecord(user,ref,trans_type,service,destination, description,amount):
    return Transaction.objects.create(user=user,transaction_ref=ref,type=trans_type,service=service,destination=destination,description=description,amount=amount)

def DecrementWallet(user,amount):
    user.profile.wallet_balance -= Decimal(amount)
    user.profile.wallet_out += Decimal(amount) 
    user.save()
    return True
    # return User.objects.filter(username=user.username).update(user.profile.wallet_balance=final_bal)

def DescA(network):
    if int(network) == 15:
        return "MTN VTU"
    elif int(network) == 20:
        return "MTN AWUFU"
    elif int(network) == 6:
        return "GLO"
    elif int(network) == 1:
        return "Airtel"
    elif int(network) == 2:
        return "9Mobile"
    

def DescD(network,category):
    if int(network) == 1 and category=="Cooperate":
        return "MTN GIFTING"
    else:
        return "MTN SME"
    
def CheckNetwork(network):
    if network == "mtn":
        return 15
    elif network == "glo":
        return 6
    elif network == "airtel":
        return 1
    elif network == '9mobile':
        return 2
    
def sendMail(subject,message,email_to, email_from='no-reply@chikjibportal.com'):
    send_mail(subject,message,email_from,[email_to],fail_silently=False)
    return True

    
def site_links(request):
    website_name = "Chikjib Portal"
    site_link = "https://chikjibportal.com"
    website_link = "https://chikjibportal.com"
    site_email = "info@chikjibportal.com"
    site_phone = "09050026406"
    created_by = "Chikjib"
    return {
       "website_name":website_name,
       "site_link": site_link,
       "website_link": website_link,
       "site_email": site_email,
       "site_phone":site_phone,
       "created_by":created_by 
    }
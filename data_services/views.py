from decimal import Decimal
from unicodedata import decimal
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from .models import AirtelProductList, ProductList 
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from dashboard import custom_helpers as h 




    
    
@login_required
@transaction.atomic
def DataTopUp(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        network = request.POST.get('network')
        phone = request.POST.get('phone')
        product_code = request.POST.get('dsize')
    
        product = ProductList.objects.filter(product_code=product_code).first()
        # print(product.quantity)
        dsize = str(product.quantity)
        
        category = product.category.name
                  
        amount = product.price
        
        # check if there is money in wallet
        
        desc = h.DescD(network=network,category=product.category)
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api
            # print(product.quantity)
            if category == "Cooperate":
                response = requests.get('https://mobileairtimeng.com/httpapi/cdatashare?userid='+api_user_id+'&pass='+api_password+'&network='+network+'&phone='+phone+'&datasize='+dsize+'&user_ref='+user_ref+'&jsn=json')
                
                data = response.json()
                # print(data)
                
            elif category=="Sme":
                response = requests.get('https://mobileairtimeng.com/httpapi/datashare?userid='+api_user_id+'&pass='+api_password+'&network='+network+'&phone='+phone+'&datasize='+dsize+'&user_ref='+user_ref+'&jsn=json')
                
                data = response.json()
                 
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                description = "Mtn Data Purchase "+ desc + " N"+str(amount)
                if category == "Cooperate":
                    service = "Cooperate Data"
                else:
                    service = "SME"
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=phone,description=description,amount=amount)
                h.DecrementWallet(user=request.user,amount=amount)
                    
                data_response = {
                    'message':data['message']
                }
                return JsonResponse(data_response,status=200)
                    
                    
            elif data['code'] == 101:
                data_response = {
                    'message':data['message']
                }
                return JsonResponse(data_response,status=404)
                
                
            else:
                data_response = {
                    'message':"An error occurred!"
                }
                return JsonResponse(data_response,status=404)
        
    products = ProductList.objects.all()
    page_title = "Mtn Datashare" 
    
    context = {
      "products":products,
      "page_title":page_title       
    }
                
    
    return render(request,'data_services/data.html',context)


@login_required
@transaction.atomic
def aDataTopUp(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        network = request.POST.get('network')
        phone = request.POST.get('phone')
        product_code = request.POST.get('dsize')
    
        product = AirtelProductList.objects.filter(product_code=product_code).first()
        # print(product.quantity)
        dsize = str(product.quantity)
        
                  
        amount = product.price
        
        # check if there is money in wallet
        
        desc = h.DescD(network=network,category="None")
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api
            # print(product.quantity)
            
            response = requests.get('https://mobileairtimeng.com/httpapi/airtel_data_share?userid='+api_user_id+'&pass='+api_password+'&network='+network+'&phone='+phone+'&datasize='+dsize+'&user_ref='+user_ref+'&jsn=json')
                
            data = response.json()
                 
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                description = "Airtel Datashare Purchase "+ desc+ " N"+str(amount)
                
                service = "AIRTEL DATA SME"
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=phone,description=description,amount=amount)
                h.DecrementWallet(user=request.user,amount=amount)
                    
                data_response = {
                    'message':data['message']
                }
                return JsonResponse(data_response,status=200)
                    
                    
            elif data['code'] == 101:
                data_response = {
                    'message':data['message']
                }
                return JsonResponse(data_response,status=404)
                
                
            else:
                data_response = {
                    'message':"An error occurred!"
                }
                return JsonResponse(data_response,status=404)
        
    products = AirtelProductList.objects.all()
    page_title = "Airtel Datashare" 
    
    context = {
      "products":products,
      "page_title":page_title          
    }
                
    
    return render(request,'data_services/adata.html',context)
    
        
@login_required
@transaction.atomic       
def getbundleList(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        network = request.POST.get('network')
        
        if network == "mtn":
            response = requests.get('https://mobileairtimeng.com/httpapi/get-items?userid='+api_user_id+'&pass='+api_password+'&service=mtn')
                
            data = response.json()
                # print(data)
                
        elif network == "etisalat":
            response = requests.get('https://mobileairtimeng.com/httpapi/get-items?userid='+api_user_id+'&pass='+api_password+'&service=9mobile')
                
            data = response.json()
                # print(data)
                 
        elif network == "airtel":
            response = requests.get('https://mobileairtimeng.com/httpapi/get-items?userid='+api_user_id+'&pass='+api_password+'&service=airtel')
                
            data = response.json()
            
        elif network == "glo":
            response = requests.get('https://mobileairtimeng.com/httpapi/get-items?userid='+api_user_id+'&pass='+api_password+'&service=glo')
                
            data = response.json()
                
        # print(data)
               
            # Finish up
            # print(data['code'])
            
            
            
        return JsonResponse(data,status=200)
                
                
    
@login_required
@transaction.atomic
def DirectDataTopUp(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        network = h.CheckNetwork(request.POST.get('network'))
        phone = request.POST.get('phone')
 
        description1 = request.POST.get('desc')
        desc = description1.split("=")[0]
                  
        amount = request.POST.get('bundles')
        
        # check if there is money in wallet
        
        print(network)
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api
        
            response = requests.get('https://mobileairtimeng.com/httpapi/datatopup?userid='+api_user_id+'&pass='+api_password+'&network='+str(network)+'&phone='+phone+'&amt='+amount+'&jsn=json')
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                service = "Data"
                description = "Data Purchase "+ desc+ " N"+str(amount)
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=phone,description=description,amount=amount)
                h.DecrementWallet(user=request.user,amount=amount)
                    
                data_response = {
                    'message':data['message']
                }
                return JsonResponse(data_response,status=200)
                    
                    
            elif data['code'] == 101:
                data_response = {
                    'message':data['message']
                }
                return JsonResponse(data_response,status=404)
                
                
            else:
                data_response = {
                    'message':"An error occurred!"
                }
                return JsonResponse(data_response,status=404)
        
                
    page_title = "Data Bundle Topup" 
    context = {
        "page_title":page_title
    }
    return render(request,'data_services/d_data.html',context)
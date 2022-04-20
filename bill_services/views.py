from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.db import transaction
from dashboard import custom_helpers as h   
        
@login_required
@transaction.atomic       
def customerCheck(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        bill = request.POST.get('bill')
        smartno = request.POST.get('smartno')

        
        response = requests.get('https://mobileairtimeng.com/httpapi/customercheck?userid='+api_user_id+'&pass='+api_password+'&bill='+bill+'&smartno='+smartno+'&jsn=json')
                
        data = response.json()
        print(data)
        
        return JsonResponse(data,status=200)
                
                
    
@login_required
@transaction.atomic
def Startimes(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        amount = request.POST.get('samt')
        phone = request.POST.get('phone')
        smartno = request.POST.get('ssmart')
        description1 = request.POST.get('desc')
        desc = description1.split("=")[0]
        
        amount = amount.split('|')[1]
                          
        # check if there is money in wallet
        
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api

            response = requests.get('https://mobileairtimeng.com/httpapi/startimes?userid='+api_user_id+'&pass='+api_password+'&phone='+phone+'&amt='+amount+'&jsn=json&user_ref='+user_ref)
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                service = "Startimes"
                description = "Bill Payment "+ desc+ " N"+amount
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=smartno,description=description,amount=amount)
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
        
                
    page_title = "Startimes" 
    context = {
        "page_title":page_title
    }
    return render(request,'bill_services/startimes.html',context)


@login_required
@transaction.atomic
def Gotv(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        amount = request.POST.get('samt')
        phone = request.POST.get('phone')
        billtype = "gotv"
        customer = request.POST.get('goname')
        invoice = request.POST.get('goinvoice')
        customernumber = request.POST.get('gocustno')
        smartno = request.POST.get('ssmart')
        description1 = request.POST.get('desc')
        desc = description1.split("=")[0]
        
        amount = amount.split('|')[0]
                          
        # check if there is money in wallet
        
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api


            response = requests.get('https://mobileairtimeng.com/httpapi/multichoice?userid='+api_user_id+'&pass='+api_password+'&phone='+phone+'&smartno='+smartno+'&customer='+customer+'&invoice='+invoice+'&billtype='+billtype+'&customernumber='+customernumber+'&jsn=json')
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                service = "Gotv"
                description = "Bill Payment "+ desc+ " N"+amount
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=smartno,description=description,amount=amount)
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
        
                
    page_title = "Gotv" 
    context = {
        "page_title":page_title
    }
    return render(request,'bill_services/gotv.html',context)


@login_required
@transaction.atomic
def Dstv(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        amount = request.POST.get('samt')
        phone = request.POST.get('phone')
        billtype = "dstv"
        customer = request.POST.get('goname')
        invoice = request.POST.get('goinvoice')
        customernumber = request.POST.get('gocustno')
        smartno = request.POST.get('ssmart')
        description1 = request.POST.get('desc')
        desc = description1.split("=")[0]
        
        amount = amount.split('|')[0]
                          
        # check if there is money in wallet
        
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api


            response = requests.get('https://mobileairtimeng.com/httpapi/multichoice?userid='+api_user_id+'&pass='+api_password+'&phone='+phone+'&smartno='+smartno+'&customer='+customer+'&invoice='+invoice+'&billtype='+billtype+'&customernumber='+customernumber+'&jsn=json')
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                service = "Dstv"
                description = "Bill Payment "+ desc+ " N"+amount
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=smartno,description=description,amount=amount)
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
        
                
    page_title = "Dstv" 
    context = {
        "page_title":page_title
    }
    return render(request,'bill_services/dstv.html',context)

# Electricity
@login_required
@transaction.atomic       
def electricityCheck(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        service = request.POST.get('service')
        meterno = request.POST.get('meterno')

        
        response = requests.get('https://mobileairtimeng.com/httpapi/power-validate?userid='+api_user_id+'&pass='+api_password+'&service='+service+'&meterno='+meterno+'&jsn=json')
                
        data = response.json()
        print(data)
        
        return JsonResponse(data,status=200)
    
@login_required
@transaction.atomic       
def electricityList(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD

        
        response = requests.get('https://mobileairtimeng.com/httpapi/power-lists?userid='+api_user_id+'&pass='+api_password)
                
        data = response.json()
        print(data)
        
        return JsonResponse(data,status=200)
    


@login_required
@transaction.atomic
def PayElectricity(request):
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
        amount = request.POST.get('amount')
        service = request.POST.get('service')
        meterno = request.POST.get('meterno')
        mtype = request.POST.get('mtype')
        
        
        
                          
        # check if there is money in wallet
        
        
        # print(desc)
        checkbal = h.CheckBalance(user = request.user, amount = amount)
        
        
        if checkbal == True:
            data = {
                'message':"Insufficient Funds!"
            }
            return JsonResponse(data,status=200)
           
        else:   
        # Run the api

            response = requests.get('https://mobileairtimeng.com/httpapi/power-pay?userid='+api_user_id+'&pass='+api_password+'&service='+service+'&meterno='+meterno+'&mtype='+mtype+'&amt='+amount+'&jsn=json')
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
               
                description = "Bill Payment Meter No: " +data['meterno']+ " Pin Code: "+ data['pincode'] + " Pin Message: " +data['pinmessage']+ " N"+amount
                    
                h.TakeRecord(user = request.user, ref=data['user_ref'] or user_ref,trans_type=trans_type,service=service,destination=meterno,description=description,amount=amount)
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
        
                
    page_title = "Electricity" 
    context = {
        "page_title":page_title
    }
    return render(request,'bill_services/electricity.html',context)
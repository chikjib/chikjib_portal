from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from django.db import transaction
from dashboard import custom_helpers as h  
from .models import Education

@login_required
@transaction.atomic
def Waec(request):
    education = Education.objects.filter(name='waec').first()
    amount = education.amount 
    
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
                        
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

            response = requests.get('https://mobileairtimeng.com/httpapi/waecdirect?userid='+api_user_id+'&pass='+api_password+'&jsn=json&user_ref='+user_ref)
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                service = "Waec"
                description = "Card Pin Payment, Serial No: "+ data['serial_no']+ " Pin: "+data['pin']+"  N"+amount
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,description=description,amount=amount)
                h.sendMail(subject="Waec Pin Purchase",message=description,email_to=[request.user.email])
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
    page_title = "Waec Result Checker Pin" 
    
    context = {
        'amount':amount,
        "page_title":page_title
    }           
    
    return render(request,'education/waec.html',context)

@login_required
@transaction.atomic
def Neco(request):
    education = Education.objects.filter(name='neco').first()
    amount = education.amount 
    if request.method == "POST":
        api_user_id = settings.API_USER_ID
        api_password = settings.API_PASSWORD
        user_ref = get_random_string(length=8)
                        
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

            response = requests.get('https://mobileairtimeng.com/httpapi/neco?userid='+api_user_id+'&pass='+api_password+'&jsn=json&user_ref='+user_ref)
                
            data = response.json()
            print(data)
                
            
                  
                # print(data)
            # Finish up
            # print(data['code'])
            
            
            if data['code'] == 100:
                trans_type = "Debit"
                service = "Neco"
                description = "Card Pin Payment, Pin: "+data['pin']+"  N"+amount
                    
                h.TakeRecord(user = request.user, ref=user_ref,trans_type=trans_type,service=service,destination=request.user.email,description=description,amount=amount)
                
                h.sendMail(subject="Neco Pin Purchase",message=description,email_to=[request.user.email])

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
        
    page_title = "Neco Result Pin" 
               
    context = {
        'amount':amount,
        "page_title":page_title
    }   
    
    return render(request,'education/neco.html',context)

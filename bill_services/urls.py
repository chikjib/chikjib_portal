from django.urls import path,include
from .views import Dstv, Gotv, PayElectricity, Startimes, customerCheck, electricityCheck, electricityList

urlpatterns = [
    path('check-customer/',customerCheck,name="check_customer"),
    path('startimes/',Startimes,name="startimes"),
    path('gotv/',Gotv,name="gotv"),
    path('dstv/',Dstv,name="dstv"),
    path('power-validate/',electricityCheck,name="power"),
    path('power-list/',electricityList,name="power_list"),
    path('power-pay/',PayElectricity,name="power_pay"),
]
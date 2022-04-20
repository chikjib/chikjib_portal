from django.urls import path,include

from education.views import Neco, Waec

urlpatterns = [
    path('waec/',Waec,name="waec"),
    path('neco/',Neco,name="neco"),
]
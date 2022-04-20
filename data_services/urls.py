from django.urls import path,include

from data_services.views import DataTopUp,DirectDataTopUp, aDataTopUp, getbundleList


urlpatterns = [
    path('mtn_datashare/',DataTopUp,name="data"),
    path('airtel_datashare/',aDataTopUp,name="adata"),
    path('get-bundle-list/',getbundleList,name="bundle-list"),
    path('direct-data-topup/',DirectDataTopUp,name="direct_data")
]
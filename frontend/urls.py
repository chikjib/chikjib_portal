from django.urls import path,include

from frontend.views import Home


urlpatterns = [
    path('',Home.as_view(),name="home"),
]
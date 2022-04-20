from django.urls import path,include
from accounts.views import MyLoginView, ProfileView, RegisterView

from frontend.views import Home
from django.contrib.auth.views import PasswordChangeView


urlpatterns = [
    path('',Home.as_view(),name="home"),
    path('login/', MyLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', RegisterView, name='register'),
    path('profile/',ProfileView,name='profile'),
    path('password_change/',PasswordChangeView.as_view(
            template_name='registration/change_password.html',
        ),
        name='change_password'
    ),
]
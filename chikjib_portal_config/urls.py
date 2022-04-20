"""chikjib_portal_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

# Adds site header, site title, index title to the admin side.
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.SITE_INDEX_TITLE

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',include('frontend.urls')),
    path('',include('dashboard.urls')),
    path('',include('airtime_services.urls')),
    path('',include('data_services.urls')),
    path('',include('bill_services.urls')),
    path('',include('education.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
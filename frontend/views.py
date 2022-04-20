from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView

class Home(TemplateView):
    template_name = "frontend/index.html"
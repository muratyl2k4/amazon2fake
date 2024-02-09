from django.urls import path 
from .views import kargotakip

urlpatterns = [
    path("kargotakip" , kargotakip)
]
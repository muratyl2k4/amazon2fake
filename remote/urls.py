from django.urls import path
from .views import fbaHomePage , fbaMarketPage, fbaMarketPoolPage , fbaMarketDeletedPage
from django.views.generic import TemplateView

urlpatterns = [
    path('' , TemplateView.as_view(template_name='home.html') , name='home'),
    path("ss" , fbaHomePage , name='sshome'),
    path("fba" , fbaHomePage),
    path("fba/<str:country>" , fbaMarketPage),
    path("fba/<str:country>/pool" , fbaMarketPoolPage),
    path("fba/<str:country>/deleted" , fbaMarketDeletedPage),
]

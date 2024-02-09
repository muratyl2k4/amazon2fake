from django.urls import path
from .views import home , pl , muhasebe  , dbdownload , ingiltere , almanya , fransa
urlpatterns = [
    path("" , home , name="home"),
    path("home" , home),
    path("pl" , pl),
    path("muhasebe" , muhasebe),
    path("ingiltere" , ingiltere ),
    path("almanya" , almanya),
    path("fransa" , fransa),
    path("downloadfile/<str:country>" , dbdownload)
]
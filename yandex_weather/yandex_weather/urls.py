
from django.urls import path
from weatherapp.views import weather_detail


urlpatterns = [
    path('weather/', weather_detail, name='weather_detail'),
]

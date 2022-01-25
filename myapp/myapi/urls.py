from django.urls import path
from .views import (WeatherView, WeatherViewCities, WeatherViewCitiesCSV,
                    UserRegistration, Root)

urlpatterns = [
    path('', Root.as_view()),
    path('user/', UserRegistration.as_view()),
    path('weather/', WeatherView.as_view()),
    path('export_to_json/', WeatherViewCities.as_view()),
    path('export_to_csv/', WeatherViewCitiesCSV.as_view()),
]

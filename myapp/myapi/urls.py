from django.urls import path

from .views import (Root, UserRegistration, WeatherView, WeatherViewCities,
                    WeatherViewCitiesCSV)

urlpatterns = [
    path('', Root.as_view()),
    path('user/', UserRegistration.as_view()),
    path('weather/', WeatherView.as_view()),
    path('export_to_json/', WeatherViewCities.as_view()),
    path('export_to_csv/', WeatherViewCitiesCSV.as_view()),
]

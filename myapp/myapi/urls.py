from django.urls import path

from .views import UserRegistration, WeatherCitiesCsvView, WeatherView

urlpatterns = [
    path('user', UserRegistration.as_view()),
    path('weather', WeatherView.as_view()),
    path('export_to_csv', WeatherCitiesCsvView.as_view()),
]

from django.contrib import admin

from .models import WeatherCity, TopCities

admin.site.register(WeatherCity)
admin.site.register(TopCities)

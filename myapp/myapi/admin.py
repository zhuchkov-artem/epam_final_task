from django.contrib import admin

from .models import TopCities, WeatherCity

admin.site.register(WeatherCity)
admin.site.register(TopCities)

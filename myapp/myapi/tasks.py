import json
from datetime import datetime

from celery import shared_task

from .models import TopCities, WeatherCity
from .views import ACTIVE_SERVICE_CLASS


@shared_task()
def collect_weather_for_top_cities():
    """
    Celery background task for collecting weather forecast for top cities.
    """
    for city in TopCities.objects.all():
        city_name = city.city
        response = ACTIVE_SERVICE_CLASS.get_city_weather(city=city_name,
                                                         units='metric')
        WeatherCity(city=city_name, date=datetime.now,
                    weather=json.loads(response.text)).save()

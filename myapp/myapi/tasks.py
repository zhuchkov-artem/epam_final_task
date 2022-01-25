import json
from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import TopCities, WeatherCity
from .serializers import TopCitiesSerializer
from .services import ExternalWeatherRequest

logger = get_task_logger(__name__)


@shared_task()
def collect_weather_for_top_100_cities():
    """Celery task for collecting weather forecast for top 100 cities."""
    for city in TopCities.objects.all():
        city_name = index.city
        response = ExternalWeatherRequest.get_city_weather(city=city_name,
                                                           units='metric')
        WeatherCity(city=city_name, date=datetime.now,
                    weather=json.loads(response.text)).save()

    return 'task collect_weather_for_top_100_cities is successful'

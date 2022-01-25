from celery import shared_task
from celery.utils.log import get_task_logger

from .models import WeatherCity
from .services import add_top_100_cities_weather_to_db, ExternalWeatherRequest


logger = get_task_logger(__name__)


@shared_task()
def collect_weather_for_top_100_cities():
    """Celery task for collecting weather forecast for top 100 cities."""
    weather = ExternalWeatherRequest.get_weather_top_cities()
    add_top_100_cities_weather_to_db(weather, WeatherCity)
    return 'task add_information_about_weather is successful'

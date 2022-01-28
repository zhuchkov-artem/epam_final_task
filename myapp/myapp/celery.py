import json
import os
from datetime import datetime

from celery import Celery

from myapp.myapi.models import TopCities, WeatherCity
from myapp.myapi.views import ACTIVE_SERVICE_CLASS

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

app = Celery('myapp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, collect_weather_for_top_cities.s(),
                             name='collect weather')


@app.task
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

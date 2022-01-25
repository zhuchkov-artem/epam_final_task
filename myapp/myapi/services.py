import csv
import json
import time
from abc import ABC, abstractmethod

import requests
from django.conf import settings
from django.http import StreamingHttpResponse

from .models import WeatherCity


class ExternalWeatherRequest(ABC):
    """Abstract base class for weather service classes."""
    @classmethod
    @abstractmethod
    def generate_api_url(cls, city, units):
        """Create api url considering peculiarities of weather source"""

    @classmethod
    def get_city_weather(cls, city, units):
        """
        Get weather forecast for the city.
        units='metric' for temperature in Celsius
        units='imperial' for temperature in Fahrenheits
        """
        time.sleep(1)  # External API call timeout
        api_url = cls.generate_api_url(city, units)
        response = requests.get(api_url)
        if response.ok:
            return json.loads(response.text)
        return None


class OpenWeatherMap(ExternalWeatherRequest):
    """Weather service class for openweathermap.org API."""
    api_key = getattr(settings, 'OPEN_WEATHER_MAP_API_KEY')
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    @classmethod
    def generate_api_url(cls, city, units):
        parameters = f'?q={city}&units={units}&appid={cls.api_key}'
        return cls.base_url + parameters


class WeatherStack(ExternalWeatherRequest):
    """Weather service class for weatherstack.com API."""

    api_key = getattr(settings, 'WEATHER_STACK_API_KEY')
    base_url = 'http://api.weatherstack.com/current'

    @classmethod
    def generate_api_url(cls, city, units):
        units = 'm' if units == 'metric' else 'f'
        parameters = f'?query={city}&units={units}&access_key={cls.api_key}'
        return cls.base_url + parameters


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csv_response(datetime_first, datetime_last):
    """
    Generate Http Response with .csv file
    """
    weathers = WeatherCity.objects.filter(date__gte=datetime_first,
                                          date__lte=datetime_last)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    csv_data = (writer.writerow([weather.city,
                                 weather.date,
                                 weather.weather]) for weather in weathers)
    response = StreamingHttpResponse(csv_data, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response

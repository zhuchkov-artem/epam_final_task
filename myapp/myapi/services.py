import csv
import requests
import json
import time
from abc import ABC, abstractmethod

from datetime import datetime
from django.http import StreamingHttpResponse

from .models import WeatherCity, TopCities
from .serializers import WeatherCitySerializer, TopCitiesSerializer
from django.conf import settings


class ExternalWeatherRequest(ABC):

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
        api_url = cls.generate_api_url(city, units)
        response = requests.get(api_url)
        if response.ok:
            return json.loads(response.text)

    @classmethod
    def get_weather_top_cities(cls):
        """
        Get weather forecast for 100 most populated cities.
        """
        weather_top_cities = []
        cities = TopCities.objects.all()
        serializer = TopCitiesSerializer(cities, many=True)
        for index in serializer.data:
            city = index['city']
            response = cls.get_city_weather(city=city, units='metric')
            weather_top_cities.append({'city': city,
                                       'date': datetime.now(),
                                       'weather': json.loads(response.text)})
            time.sleep(1)  # API call timeout
        return weather_top_cities


class OpenWeatherMap(ExternalWeatherRequest):

    api_key = getattr(settings, 'OPEN_WEATHER_MAP_API_KEY')
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    @classmethod
    def generate_api_url(cls, city, units):
        parameters = f'?q={city}&units={units}&appid={cls.api_key}'
        return cls.base_url + parameters


class WeatherStack(ExternalWeatherRequest):

    api_key = getattr(settings, 'WEATHER_STACK_API_KEY')
    base_url = 'http://api.weatherstack.com/current'

    @classmethod
    def generate_api_url(cls, city, units):
        units = 'm' if units == 'metric' else 'f'
        parameters = f'?query={city}&units={units}&access_key={cls.api_key}'
        return cls.base_url + parameters


def add_top_100_cities_weather_to_db(weather_info, weather):
    """Save weather information into database"""
    for info in weather_info:
        try:
            weather(city=info['city'],
                    date=info['date'],
                    weather=info['weather']).save()
        except TypeError:
            pass


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_to_csv_from_database(date_begin, date_end):
    """this function used for get information from
    database and write it into csv dict"""
    weathers = WeatherCity.objects.filter(date__gte=date_begin,
                                          date__lte=date_end)
    serializer = WeatherCitySerializer(weathers, many=True)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow([weather['city'], weather['date'], weather['weather']]) for weather in serializer.data), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response

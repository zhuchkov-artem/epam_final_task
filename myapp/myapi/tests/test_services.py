import json
from unittest.mock import patch

import requests
from django.test import TestCase

from .. import services
from ..services import ExternalWeatherRequest, OpenWeatherMap, WeatherStack


class FakeResponse:
    def __init__(self, url):
        self.url = url
        self.ok = True
        self.text = json.dumps({'Temperature': '-10', 'Feels like': '-13'})


def test_api_url(city, units):
    return f'test.weather.api?city={city}&units={units}'


class ExternalWeatherRequestTest(TestCase):

    def test_get_city_weather(self):
        with patch.object(ExternalWeatherRequest, 'generate_api_url',
                          test_api_url):
            with patch.object(requests, 'get', FakeResponse):
                weather = ExternalWeatherRequest.get_city_weather('Moscow',
                                                                  'metric')
        self.assertEquals(weather, {'Temperature': '-10', 'Feels like': '-13'})


class OpenWeatherMapTest(TestCase):

    def test_generate_api_url(self):
        city, units, api_key = 'Moscow', 'metric', 'qwerty'
        expected_url = f'http://api.openweathermap.org/data/2.5/' \
                       f'weather?q={city}&units={units}&appid={api_key}'
        with patch.object(services.OpenWeatherMap, 'api_key', api_key):
            url = OpenWeatherMap.generate_api_url(city, units)
        self.assertEquals(url, expected_url)


class WeatherStackTest(TestCase):

    def test_generate_api_url(self):
        city, units, api_key = 'Moscow', 'metric', 'qwerty'
        expected_url = f'http://api.weatherstack.com/current' \
                       f'?query={city}&units=m&access_key={api_key}'
        with patch.object(services.WeatherStack, 'api_key', api_key):
            url = WeatherStack.generate_api_url(city, units)
        self.assertEquals(url, expected_url)

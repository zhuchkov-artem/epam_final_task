import datetime

from django.test import TestCase

from ..models import TopCities, WeatherCity


class WeatherCityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        WeatherCity.objects.create(city='Khabarovsk',
                                   date=datetime.datetime.now(),
                                   weather='+30')

    def test_city_label(self):
        weather = WeatherCity.objects.get(city='Khabarovsk')
        field_label = weather._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_city_max_length(self):
        weather = WeatherCity.objects.get(city='Khabarovsk')
        max_length = weather._meta.get_field('city').max_length
        self.assertEquals(max_length, 50)

    def test_date_label(self):
        weather = WeatherCity.objects.get(city='Khabarovsk')
        field_label = weather._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')

    def test_weather_label(self):
        weather = WeatherCity.objects.get(city='Khabarovsk')
        field_label = weather._meta.get_field('weather').verbose_name
        self.assertEquals(field_label, 'weather')

    def test_object_name(self):
        weather = WeatherCity.objects.get(city='Khabarovsk')
        expected_object_name = f'{weather.city} ' \
                               f'[{weather.date}] ' \
                               f'{weather.weather}'
        self.assertEquals(expected_object_name, str(weather))


class TopCityModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        TopCities.objects.create(city='Khabarovsk')

    def test_city_label(self):
        top_city = TopCities.objects.get(city='Khabarovsk')
        field_label = top_city._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'city')

    def test_object_name(self):
        top_city = TopCities.objects.get(city='Khabarovsk')
        expected_object_name = f'{top_city.city}'
        self.assertEquals(expected_object_name, str(top_city))

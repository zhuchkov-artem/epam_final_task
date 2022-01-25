from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WeatherCity
from .services import export_to_csv_from_database
from . import services
from .serializers import (WeatherCitySerializer, UserSerializer,
                          DateTimeSerializer, CityUnitsSerializer)


CACHE_TTL = getattr(settings, 'CACHE_TTL')
ACTIVE_WEATHER_SOURCE = getattr(settings, 'ACTIVE_WEATHER_SOURCE')
ACTIVE_SERVICE_CLASS = getattr(services, ACTIVE_WEATHER_SOURCE)


class WeatherView(APIView):
    """This view automatically generate information about city."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """
        Give city weather forecast.
        Use units=metric for Celsius and units=imperial for Fahrenheit
        Request example:
        weather?city=Moscow&units=metric
        """
        if 'city' in request.GET and 'units' in request.GET:
            city = request.GET['city']
            units = request.GET['units']
            serializer = CityUnitsSerializer(data={'city': city, 'units': units})
            if serializer.is_valid():
                weather = ACTIVE_SERVICE_CLASS.get_city_weather(
                    serializer.data['city'],
                    serializer.data['units'])
                if weather:
                    return Response(weather, status=status.HTTP_200_OK)
        return Response('BadRequest', status=status.HTTP_400_BAD_REQUEST)


class WeatherViewCities(APIView):
    """
    This view automatically generate information about 100 cities in
    json ordered by population
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """
        Give information about 100 top cities weather
        between date_first and date_last in json format.
        Use date_first and date_last in format 'YYYY-MM-DD'
        Request example:
        export_to_json?date_first=2021-06-15&date_last=2022-01-01
        """
        if 'date_first' in request.GET and 'date_last' in request.GET:
            serializer = DateTimeSerializer(
                data={'date_first': request.GET['date_first'],
                      'date_last': request.GET['date_last']})
            if serializer.is_valid():
                weathers = WeatherCity.objects.filter(
                    date__gte=serializer.data['date_first'],
                    date__lte=serializer.data['date_last'])
                serializer = WeatherCitySerializer(weathers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('BadRequest', status=status.HTTP_400_BAD_REQUEST)


class WeatherViewCitiesCSV(APIView):
    """
    This view automatically generate information about 100 cities
    in csv file ordered by population
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        """
        Give information about 100 top cities weather
        between date_first and date_last in csv file format.
        Use date_first and date_last in format 'YYYY-MM-DD'
        Request example:
        export_to_csv?date_first=2021-06-15&date_last=2022-01-01
        """
        if 'date_first' in request.GET and 'date_last' in request.GET:
            serializer = DateTimeSerializer(
                data={'date_first': request.GET['date_first'],
                      'date_last': request.GET['date_last']})
            if serializer.is_valid():
                return export_to_csv_from_database(
                    serializer.data['date_first'],
                    serializer.data['date_last'])
        return Response('BadRequest', status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    """
    For registration use username and password
    """

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Root(APIView):
    """My API ROOT"""
    def get(self, request, format=None):
        return Response({'docs': 'http://0.0.0.0:8000/api/docs',
                         'login': 'http://0.0.0.0:8000/api-auth/login'})

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import (CityUnitsSerializer, DateTimeSerializer,
                          UserSerializer)
from .services import csv_response

ACTIVE_WEATHER_SOURCE = getattr(settings, 'ACTIVE_WEATHER_SOURCE')
ACTIVE_SERVICE_CLASS = getattr(services, ACTIVE_WEATHER_SOURCE)


class UserRegistration(APIView):
    """
    For registration use username and password
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class WeatherView(APIView):
    """API View for /api/weather urlpattern"""

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get(self, request):
        """
        Give city weather forecast.
        Use units=metric for Celsius and units=imperial for Fahrenheit
        Request example:
        weather?city=Moscow&units=metric
        """
        if 'city' in request.GET and 'units' in request.GET:
            city = request.GET['city']
            units = request.GET['units']
            serializer = CityUnitsSerializer(data={'city': city,
                                                   'units': units})
            if serializer.is_valid():
                weather = ACTIVE_SERVICE_CLASS.get_city_weather(city, units)
                if weather is not None:
                    return Response(weather, status=HTTP_200_OK)
                return Response(status=HTTP_503_SERVICE_UNAVAILABLE)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_400_BAD_REQUEST)


class WeatherCitiesCsvView(APIView):
    """API View for /api/export_to_csv urlpattern"""

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get(self, request):
        """
        Give information about 100 top cities weather between datetime_first
        and datetime_last in csv file format.
        Use 'YYYY-MM-DD-HH:MM:SS' datetime format.
        Request example:
        export_to_csv?datetime_first=2021-06-15&datetime_last=2022-01-01
        """
        if 'datetime_first' in request.GET and 'datetime_last' in request.GET:
            datetime_first = request.GET['datetime_first']
            datetime_last = request.GET['datetime_last']
            serializer = DateTimeSerializer(data={
                'datetime_first': datetime_first,
                'datetime_last': datetime_last})
            if serializer.is_valid():
                return csv_response(datetime_first, datetime_last)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_400_BAD_REQUEST)

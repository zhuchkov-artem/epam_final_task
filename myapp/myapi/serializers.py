from django.contrib.auth.models import User
from rest_framework import serializers

from .models import TopCities, WeatherCity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class WeatherCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ['city', 'date', 'weather']


# class TopCitiesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TopCities
#         fields = ['city']


class DateTimeSerializer(serializers.Serializer):
    date_first = serializers.DateTimeField()
    date_last = serializers.DateTimeField()


class CityUnitsSerializer(serializers.Serializer):
    city = serializers.CharField()
    units = serializers.ChoiceField(choices=['metric', 'imperial'])

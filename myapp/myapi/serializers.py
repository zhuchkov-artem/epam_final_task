from django.contrib.auth.models import User
from rest_framework import serializers


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


class DateTimeSerializer(serializers.Serializer):
    datetime_first = serializers.DateTimeField()
    datetime_last = serializers.DateTimeField()


class CityUnitsSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=30)
    units = serializers.ChoiceField(choices=['metric', 'imperial'])

from django.db import models


class WeatherCity(models.Model):
    """Model for storing weather in top 100 cities."""
    city = models.CharField(null=False, max_length=50)
    date = models.DateTimeField(null=False, db_index=True)
    weather = models.TextField(null=False)

    def __str__(self):
        return f'{self.city} [{self.date}] {self.weather}'


class TopCities(models.Model):
    """Model for storing top 100 city names."""
    city = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return f'{self.city}'

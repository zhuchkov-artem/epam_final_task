import requests
from bs4 import BeautifulSoup
from django.db import migrations

from ..models import TopCities


def add_top_100_cities(apps, schema_editor):
    response = requests.get('https://worldpopulationreview.com/world-cities')
    soup = BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr', limit=100)

    for tr in trs:
        TopCities(city=tr.find_all('td')[1].text).save()


def delete_top_100_cities(apps, schema_editor):
    TopCities.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_top_100_cities, delete_top_100_cities),
    ]

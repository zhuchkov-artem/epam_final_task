from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TopCities',
            fields=[
                ('city', models.CharField(max_length=30, primary_key=True,
                                          serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('date', models.DateTimeField(db_index=True)),
                ('weather', models.TextField()),
            ],
        ),
    ]

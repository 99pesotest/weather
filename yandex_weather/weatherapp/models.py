
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64)
    longitude = models.FloatField()
    latitude = models.FloatField()
    unique_identifier = models.CharField(max_length=128, unique=True, editable=False, default='default_value')

    def save(self, *args, **kwargs):
        self.unique_identifier = f"{self.name}_{self.longitude}_{self.latitude}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Weather(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    time_of_day = models.CharField(max_length=10)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city.name} - {self.time_of_day}"

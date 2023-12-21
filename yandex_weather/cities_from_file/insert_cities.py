
import sys
import os
sys.path.append("..")
from weatherapp.models import City


def populate_cities_from_file(file_path):
    print(os.listdir())
    with open(file_path, 'r') as file:
        for line in file:
            city_data = line.strip().split(':')
            city_name = city_data[0]
            coordinates = city_data[1].split(',')
            latitude = float(coordinates[0])
            longitude = float(coordinates[1])

            # Создание записи в таблице City
            City.objects.create(name=city_name, latitude=latitude, longitude=longitude)


if __name__ == "__main__":
    file_path = "cities.txt"
    populate_cities_from_file(file_path)

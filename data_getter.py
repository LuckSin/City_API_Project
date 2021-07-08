import requests
import math
from typing import *

from config import API_KEYS, CURSOR, VERSION_YANDEX, CONN


def get_city_from_database(place: Optional[str] = None):
    query = 'SELECT * FROM city_project'
    if place:
        query += ' WHERE city = %s'
        city_s = (place,)
        CURSOR.execute(query, city_s)
    else:
        CURSOR.execute(query)

    city_coordinates = CURSOR.fetchall()
    if city_coordinates and place:

        return city_coordinates[0][0], city_coordinates[0][1]
    else:
        return city_coordinates


def get_city_coordinates_from_yandex_api(place):
    url = f"https://geocode-maps.yandex.ru/{VERSION_YANDEX}{API_KEYS}&format=json&geocode={place}"
    response = requests.request("GET", url)
    coordinates_list = response.json()['response']['GeoObjectCollection']['featureMember']
    if coordinates_list:
        coordinates_id = coordinates_list[0]['GeoObject']['Point']['pos'].split()
        coordinates_longitude = float(coordinates_id[0])
        coordinates_latitude = float(coordinates_id[1])

        return coordinates_longitude, coordinates_latitude
    else:
        raise Exception(f'Unknown place {place}')


def add_city_to_database(place, coordinates_longitude, coordinates_latitude):
    insert_query = "INSERT INTO city_project (city, coordinates_longitude, coordinates_latitude)" \
                   " VALUES(%s, %s, %s);"
    insert_values = (place, coordinates_longitude, coordinates_latitude)
    CURSOR.execute(insert_query, insert_values)
    CONN.commit()


def solve_distance_formula(first_coordinates, second_coordinates):
    first_place_coordinates_latitude = first_coordinates[1]
    first_place_coordinates_longitude = first_coordinates[0]
    second_place_coordinates_latitude = second_coordinates[1]
    second_place_coordinates_longitude = second_coordinates[0]
    distance_between_cities = math.acos(math.sin(first_place_coordinates_latitude * 3.14 / 180) * math.sin(
        second_place_coordinates_latitude * 3.14 / 180)
                                        + math.cos(first_place_coordinates_latitude * 3.14 / 180) * math.cos(
        second_place_coordinates_latitude * 3.14 / 180)
                                        * math.cos(
        (second_place_coordinates_longitude * 3.14 / 180 - first_place_coordinates_longitude * 3.14 / 180)))
    distance = distance_between_cities * 6371.008
    print(distance)
    return distance


def get_distance_between_cities(first_place, second_place):
    if get_city_from_database(first_place):
        first_coordinates = get_city_from_database(first_place)
    else:
        first_coordinates = get_city_coordinates_from_yandex_api(first_place)
        add_city_to_database(first_place, first_coordinates[0], first_coordinates[1])

    if get_city_from_database(second_place):
        second_coordinates = get_city_from_database(second_place)
    else:
        second_coordinates = get_city_coordinates_from_yandex_api(second_place)
        add_city_to_database(second_place, second_coordinates[0], second_coordinates[1])

    return solve_distance_formula(first_coordinates, second_coordinates)

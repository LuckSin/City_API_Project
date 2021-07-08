#!flask/bin/python
from flask import Flask, jsonify

from data_getter import (get_city_from_database,
                         get_city_coordinates_from_yandex_api,
                         add_city_to_database,
                         get_distance_between_cities)


app = Flask(__name__)


@app.route('/api/v1/cities', methods=['GET'])
def get_cities():
    cities = get_city_from_database()
    return jsonify({'cities': cities})


@app.route('/api/v1/city/<city>', methods=['GET'])
def get_city_by_name(city):
    if get_city_from_database(city):
        lon, lat = get_city_from_database(city)
    else:
        lon, lat = get_city_coordinates_from_yandex_api(city)
        add_city_to_database(city, lon, lat)
    all_info = city, lon, lat
    return jsonify({'city': all_info})


@app.route('/api/v1/city/<first_city>/<second_city>', methods=['POST'])
def post_distance(first_city,second_city):
    distance = get_distance_between_cities(first_city, second_city)
    return jsonify({'distance': distance})


if __name__ == '__main__':
    app.run(debug=True)

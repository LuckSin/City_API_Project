import pytest

from data_getter import get_city_from_database, solve_distance_formula, get_distance_between_cities
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_check_list_cities(client):
    response = client.get('/api/v1/cities')
    assert response.status_code == 200


def test_get_city(client):
    response = client.get('/api/v1/city/Minsk')
    mock_request_data = {
        "city": ["Minsk", 27.561831, 53.902284]
    }
    assert response.status_code == 200
    assert response.json == mock_request_data


def test_get_distance(client):
    response = client.post('/api/v1/city/Minsk/Kiev')
    distance = get_distance_between_cities('Minsk', 'Kiev')
    mock_request_data = {
        "distance": distance
    }
    assert response.status_code == 200
    assert response.json == mock_request_data


def test_check_city_in_db():
    lon_minsk = 53.902284
    lat_minsk = 27.561831
    assert get_city_from_database('minsk') is not False
    assert get_city_from_database('minsk')[0] == lat_minsk
    assert get_city_from_database('minsk')[1] == lon_minsk


@pytest.mark.parametrize(('place', 'not_in_db'), ((['asdfsadfsadafasdfasdfasdf', []]),
                                                  ('asdfpdfapsfdfasdkfaskfskdf', []),))
def test_check_non_existent_city(place, not_in_db):
    assert get_city_from_database(place) == not_in_db


@pytest.mark.parametrize(('first_coordinates', 'second_coordinates', 'distance'),
                         (([27.561831, 53.902284], [23.684568, 52.094246], 328.128219929438), ))
def test_solve_distance_formula(first_coordinates, second_coordinates, distance):
    assert solve_distance_formula(first_coordinates, second_coordinates) == distance

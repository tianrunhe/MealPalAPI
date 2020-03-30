import json
from unittest.mock import patch, Mock

auckland = {
    "id": "da0fa4e8-84e8-4f97-97ef-021d79e0c532",
    "objectId": "da0fa4e8-84e8-4f97-97ef-021d79e0c532",
    "state": "NZ",
    "name": "Auckland",
    "city_code": "AKL",
    "latitude": "-36.8485",
    "longitude": "174.7633",
    "timezone": 13,
    "countryCode": "nzl",
    "countryCodeAlphaTwo": "nz",
    "defaultLocale": "en-NZ",
    "dinner": False,
    "neighborhoods": [
        {
            "id": "0c1c664d-853f-4655-bded-2786d62e5667",
            "name": "CBD"
        }
    ]
}
austin = {
    "id": "e1e2ccc2-9f4a-481d-afc6-33f1ac52ab06",
    "objectId": "e1e2ccc2-9f4a-481d-afc6-33f1ac52ab06",
    "state": "TX",
    "name": "Austin",
    "city_code": "ATX",
    "latitude": "30.2672",
    "longitude": "-97.7431",
    "timezone": -5,
    "countryCode": "usa",
    "countryCodeAlphaTwo": "us",
    "defaultLocale": "en-US",
    "dinner": False,
    "neighborhoods": [
        {
            "id": "55d394e1-2cc5-41f0-83f4-5c77ede3ec17",
            "name": "Downtown"
        },
        {
            "id": "fd9fcdd1-0492-46fc-aed0-066fd954cb01",
            "name": "UT"
        }
    ]
}

fake_cities_data = {'result': [auckland, austin]}


def test_get_cities(client):
    with patch("mealpal.blueprints.city.requests") as patched_requests:
        patched_requests.post.return_value = Mock(ok=True)
        patched_requests.post.return_value.json.return_value = fake_cities_data

        response = client.get('/cities')

        assert response.status_code == 200
        assert fake_cities_data['result'] == json.loads(response.get_data(as_text=True))


def test_get_city(client):
    with patch("mealpal.blueprints.city.requests") as patched_requests:
        patched_requests.post.return_value = Mock(ok=True)
        patched_requests.post.return_value.json.return_value = fake_cities_data

        response = client.get(F"/city/{auckland['id']}")

        assert response.status_code == 200
        assert auckland == json.loads(response.get_data(as_text=True))


def test_get_city_without_city_id(client):
    response = client.get('/city')
    assert response.status_code == 404

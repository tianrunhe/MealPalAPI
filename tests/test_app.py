from unittest.mock import Mock
from unittest.mock import patch


def test_find_and_sorted_by_distance(client, google_maps_helper):
    with patch('mealpal.blueprints.meal.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=True)
        schedule = {
            "restaurant": {
                "id": "1",
                "address": "address",
                "city": {
                    "name": "Seattle"
                },
                "neighborhood": {
                    "id": "1",
                    "name": "Downtown"
                },
                "state": "WA"
            }
        }
        patch_requests.get.return_value.json.return_value = {
            "schedules": [
                schedule
            ]
        }

        with patch("mealpal.utils.distance_calculator.GoogleMapsHelper") as patched_google_maps_helper:
            patched_google_maps_helper.return_value = Mock()
            patched_google_maps_helper.get_walking_time.return_value = 300
            with patch('mealpal.aws.dynamodb.get_distance') as patch_get_distance:
                patch_get_distance.return_value = 10

                response = client.get('/meal/1234/1?sortedByDistanceFrom=abc')
                assert response.status_code == 200
                assert response.json == [schedule]


def test_find(client):
    with patch('mealpal.blueprints.meal.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=True)
        schedule = {
            "restaurant": {
                "id": "1",
                "address": "address",
                "city": {
                    "name": "Seattle"
                },
                "neighborhood": {
                    "id": "1",
                    "name": "Downtown"
                },
                "state": "WA"
            }
        }
        patch_requests.get.return_value.json.return_value = {
            "schedules": [
                schedule
            ]
        }

        response = client.get('/meal/1234/1')
        assert response.status_code == 200
        assert response.json == [schedule]


def test_find_and_sorted_by_distances_from_multiple_offerings(client, google_maps_helper):
    with patch('mealpal.blueprints.meal.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=True)
        schedule1 = {
            "restaurant": {
                "id": "1",
                "address": "address1",
                "city": {
                    "name": "Seattle"
                },
                "neighborhood": {
                    "id": "1",
                    "name": "Downtown"
                },
                "state": "WA"
            }
        }
        schedule2 = {
            "restaurant": {
                "id": "2",
                "address": "address2",
                "city": {
                    "name": "Seattle"
                },
                "neighborhood": {
                    "id": "1",
                    "name": "Downtown"
                },
                "state": "WA"
            }
        }
        patch_requests.get.return_value.json.return_value = {
            "schedules": [
                schedule1,
                schedule2
            ]
        }

        with patch("mealpal.utils.distance_calculator.GoogleMapsHelper") as patched_google_maps_helper:
            class MockedGoogleMapsHelper(object):
                def __init__(self, times):
                    self.times = times

                def get_walking_time(self, origin_address, destination_address):
                    val = self.times.pop()
                    return val

            patched_google_maps_helper.return_value = MockedGoogleMapsHelper([900, 300])

            with patch('mealpal.aws.dynamodb.get_distance') as patch_get_distance:
                patch_get_distance.return_value = None

                with patch('mealpal.aws.dynamodb.store_distance'):
                    response = client.get('/meal/1234/1?sortedByDistanceFrom=abc')
                    assert response.status_code == 200
                    # response should be already sorted
                    assert response.json == sorted(response.json, key=lambda r: r['walkingTimeFromOrigin'])


def test_find_no_path_parameters(client):
    response = client.get('/meal')
    assert response.status_code == 404

from unittest.mock import patch
from unittest.mock import Mock
from mealpal.main import app


def test_hello():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, world!'


def test_get_cities():
    response = app.test_client().get('/cities')

    assert response.status_code == 200
    assert b'Seattle' in response.data


def test_reserve():
    with patch('mealpal.main.requests') as patch_requests:
        mocked_response = Mock()
        patch_requests.post.return_value = mocked_response
        with patch('mealpal.utils.logging_in_manager.decrypt') as patch_decrypt:
            patch_decrypt.return_value = "MealPalAPITest"

            mocked_response.ok = True
            mocked_response.status_code = 200
            response = app.test_client().post('/reserve/1234')
            assert response.status_code == 200
            assert b'{\"success\": true}' in response.data

            mocked_response.ok = False
            mocked_response.status_code = 500
            response = app.test_client().post('/reserve/1234')
            assert response.status_code == 500
            assert b'{\"success\": false}' in response.data


def test_find():
    with patch('mealpal.main.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=False)
        schedule = {
            "restaurant": {
                "address": "address",
                "city": {
                    "name": "Seattle"
                },
                "neighborhood": {
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

        patch_requests.post.return_value = Mock(ok=True)
        patch_requests.post.return_value.json.return_value = {
            "destination_addresses": [
                "address, Seattle, WA"
            ],
            "origin_addresses": [
                "2021 7th Ave, Seattle, WA"
            ],
            "rows": [
                {
                    "elements": [
                        {
                            "distance": {
                                "text": "10km",
                                "value": 10000
                            },
                            "duration": {
                                "text": "5 minutes",
                                "value": 300
                            },
                            "status": "OK"
                        }
                    ]
                }
            ],
            "status": "OK"
        }

        with patch('mealpal.utils.logging_in_manager.decrypt') as patch_decrypt:
            patch_decrypt.return_value = "MealPalAPITest"

            response = app.test_client().post('/find/1234')
            assert response.status_code == 200
            # distance is within 10 minute walk distance, schedule should be included in response
            assert response.json == [schedule]

        patch_requests.post.return_value.json.return_value = {
            "destination_addresses": [
                "address, Seattle, WA"
            ],
            "origin_addresses": [
                "2021 7th Ave, Seattle, WA"
            ],
            "rows": [
                {
                    "elements": [
                        {
                            "distance": {
                                "text": "10km",
                                "value": 10000
                            },
                            "duration": {
                                "text": "15 minutes",
                                "value": 900
                            },
                            "status": "OK"
                        }
                    ]
                }
            ],
            "status": "OK"
        }
        with patch('mealpal.utils.logging_in_manager.decrypt') as patch_decrypt:
            patch_decrypt.return_value = "MealPalAPITest"

            response = app.test_client().post('/find/1234')
            assert response.status_code == 200
            # distance is out of 10 minute walk distance, schedule should NOT be included in response
            assert response.json == []

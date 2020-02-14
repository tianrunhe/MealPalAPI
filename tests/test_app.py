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


def test_find_with_office_address():
    with patch('mealpal.main.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=True)
        schedule = {
            "restaurant": {
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

            response = app.test_client().post('/find/1234/1?office=abc')
            assert response.status_code == 200
            assert response.json == [schedule]


def test_find_without_office_address():
    with patch('mealpal.main.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=True)
        schedule = {
            "restaurant": {
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

            response = app.test_client().post('/find/1234/1')
            assert response.status_code == 200
            assert response.json == [schedule]


def test_find_with_office_address_multiple_offerings():
    with patch('mealpal.main.requests') as patch_requests:
        patch_requests.get.return_value = Mock(ok=True)
        schedule1 = {
            "restaurant": {
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

        patch_requests.post.return_value = Mock(ok=True)
        patch_requests.post.return_value.json.side_effect = [
            {
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
            },
            {
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
                                    "text": "3km",
                                    "value": 3000
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
        ]
        with patch('mealpal.utils.logging_in_manager.decrypt') as patch_decrypt:
            patch_decrypt.return_value = "MealPalAPITest"

            response = app.test_client().post('/find/1234/1?office=abc')
            assert response.status_code == 200
            assert response.json == [schedule2, schedule1]  # schedule2 is closer to the office than schedule1


def test_find_no_path_parameters():
    response = app.test_client().get('/find')
    assert response.status_code == 404

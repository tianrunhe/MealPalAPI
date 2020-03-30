from unittest.mock import patch, Mock

import pytest


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'MealPal username is required.'),
        ('a', '', b'MealPal password is required.'),
        ('test', 'test', b'123@gmail.com'),
))
def test_login(username, password, message, client):
    with patch('mealpal.blueprints.auth.requests.post') as patch_post_requests:
        patch_post_requests.return_value = Mock()
        patch_post_requests.return_value.ok = True
        patch_post_requests.return_value.json.return_value = {
            "id": "1",
            "email": "123@gmail.com",
            "status": 3,
            "firstName": "John",
            "lastName": "Doe",
            "sessionToken": "token",
            "city": {
                "id": "1",
                "name": "Seattle",
                "city_code": "SEA",
                "countryCode": "usa",
                "className": "City",
                "objectId": "1"
            }
        }
        response = client.post(
            '/login',
            json={'username': username, 'password': password}
        )
        assert message in response.data


def test_login_failed(client):
    with patch('mealpal.blueprints.auth.requests.post') as patch_post_requests:
        patch_post_requests.return_value = Mock(ok=False)
        response = client.post(
            '/login',
            json={'username': "123", 'password': "123"}
        )
        assert b"Could not log in" in response.data

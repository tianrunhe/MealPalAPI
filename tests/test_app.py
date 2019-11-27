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

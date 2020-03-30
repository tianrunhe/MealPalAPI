import json
from unittest.mock import patch, Mock

from mealpal.constants import RESERVATIONS_URL, HEADERS, DEFAULT_PICK_UP_TIME, SOURCE


def test_reserve_without_login(client):
    response = client.put('/meal/1234')
    assert response.status_code == 401
    assert b'Request is not authorized' in response.data


def test_reserve(client):
    with patch('mealpal.blueprints.meal.requests') as patch_requests:
        mocked_response = Mock()
        patch_requests.post.return_value = mocked_response

        mocked_response.ok = True
        mocked_response.status_code = 200
        response = client.put('/meal/1234', headers={"Authorization": "123"})
        assert response.status_code == 200
        assert b'{\"success\": true}' in response.data
        expected_reservation_data = {
            'quantity': 1,
            'schedule_id': "1234",
            'pickup_time': DEFAULT_PICK_UP_TIME,
            'source': SOURCE
        }
        expected_cookie = dict(sessionToken="123")
        patch_requests.post.assert_called_with(RESERVATIONS_URL, data=json.dumps(expected_reservation_data),
                                               headers=HEADERS, cookies=expected_cookie)

        mocked_response.ok = False
        mocked_response.status_code = 500
        response = client.put('/meal/1234', headers={"Authorization": "123"})
        assert response.status_code == 500
        assert b'{\"success\": false}' in response.data
        patch_requests.post.assert_called_with(RESERVATIONS_URL, data=json.dumps(expected_reservation_data),
                                               headers=HEADERS, cookies=expected_cookie)

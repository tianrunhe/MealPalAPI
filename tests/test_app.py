from mealpal.main import app


def test_hello():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, world!'


def test_get_cities():
    response = app.test_client().get('/cities')

    assert response.status_code == 200
    assert b'Seattle' in response.data

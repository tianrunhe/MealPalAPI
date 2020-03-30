from flask import request

from mealpal.validations.log_in_validator import LoggingInJsonData

valid_data = '{"username": "123@gmail.com", "password": "1234"}'
invalid_data = '{"username": ""}'
redundant_data = '{"username": "123@gmail.com", "password": "1234", "age": 23}'


def test_valid(app):
    with app.test_request_context(method='POST', data=valid_data, content_type='application/json'):
        inputs = LoggingInJsonData(request)

        assert inputs.validate()


def test_invalid(app):
    with app.test_request_context(method='POST', data=invalid_data, content_type='application/json'):
        inputs = LoggingInJsonData(request)

        assert not inputs.validate()


def test_redundant(app):
    with app.test_request_context(method='POST', data=redundant_data, content_type='application/json'):
        inputs = LoggingInJsonData(request)

        assert inputs.validate()


def test_error_messages(app):
    with app.test_request_context(method='POST', data=invalid_data, content_type='application/json'):
        inputs = LoggingInJsonData(request)
        inputs.validate()

        assert inputs.errors == ['MealPal username is required.', 'MealPal password is required.']

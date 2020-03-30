from wtforms.validators import DataRequired
from flask_inputs import Inputs


class LoggingInJsonData(Inputs):
    json = {
        'username': [
            DataRequired('MealPal username is required.')
        ],
        'password': [
            DataRequired('MealPal password is required.')
        ],
    }

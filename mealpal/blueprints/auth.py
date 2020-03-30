import json
from functools import wraps

import requests
from flask import (
    Blueprint, g, request, jsonify, make_response)

from mealpal.constants import LOGIN_URL, HEADERS
from mealpal.validations.log_in_validator import LoggingInJsonData

bp = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        if "authorization" not in request.headers:
            return make_response('Request is not authorized', 401,
                                 {'WWW.Authentication': 'Basic realm: "login required"'})

        g.user_token = request.headers["authorization"]

        return f(*args, **kwargs)

    return decorator


@bp.route('/login', methods=['POST'])
def login():
    """Log in a registered user by adding the user info to the session."""

    # validations
    inputs = LoggingInJsonData(request)
    if not inputs.validate():
        return jsonify(success=False, errors=inputs.errors)

    login_data = request.get_json()
    mealpal_login_response = requests.post(LOGIN_URL, data=json.dumps(login_data), headers=HEADERS)

    if not mealpal_login_response.ok:
        return make_response('Could not log in', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    response_json = mealpal_login_response.json()
    g.user_token = response_json['sessionToken']

    return jsonify(response_json)


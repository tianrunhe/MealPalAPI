import requests
from flask import Blueprint, jsonify

from mealpal.constants import NEIGHBORHOODS_URL

bp = Blueprint('city', __name__)


@bp.route("/cities")
def get_cities():
    return jsonify(retrieve_cities_with_neighborhoods())


@bp.route("/city/<string:city_id>")
def get_city(city_id):
    cities_with_neighborhoods = retrieve_cities_with_neighborhoods()
    city_with_neighborhoods = next(city for city in cities_with_neighborhoods if city['id'] == city_id)
    return jsonify(city_with_neighborhoods)


def retrieve_cities_with_neighborhoods():
    response = requests.post(NEIGHBORHOODS_URL)
    return response.json()['result']

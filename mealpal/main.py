import requests
import json
import urllib.parse
from dictor import dictor
from flask import Flask
from flask import jsonify
from flask import request

from mealpal.utils.logging_in_manager import LoggingInManager

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/cities")
def get_cities():
    response = requests.post("https://secure.mealpal.com/1/functions/getCitiesWithNeighborhoods")
    data = [
        {'id': city['id'], 'name': city['name'], 'state': city['state']}
        for city in response.json()['result']
    ]
    return jsonify(data)


@app.route('/reserve/<schedule_id>', methods=['GET', 'POST'])
def reserve(schedule_id):
    with LoggingInManager() as context:
        reserve_data = {
            'quantity': 1,
            'schedule_id': schedule_id,
            'pickup_time': '12:00pm-12:15pm',
            'source': 'Web',
        }
        response = requests.post('https://secure.mealpal.com/api/v2/reservations', data=json.dumps(reserve_data),
                                 headers=LoggingInManager.HEADERS, cookies=context.cookies)
        return json.dumps({'success': response.ok}), response.status_code, {'ContentType': 'application/json'}


@app.route('/find/<city_id>', methods=['GET', 'POST'])
def find(city_id):
    with LoggingInManager() as context:
        res = requests.get('https://secure.mealpal.com/api/v1/cities/{}/product_offerings/lunch/menu'.format(city_id),
                           headers=LoggingInManager.HEADERS, cookies=context.cookies)

        office_address = request.args.get('office')

        if office_address is None:
            return jsonify(res.json()['schedules'])

        results = []
        for offering in res.json()['schedules']:
            restaurant = offering['restaurant']
            neighborhood = restaurant['neighborhood']
            if neighborhood['name'] != 'Downtown':
                continue
            destination = "{}, {}, {}".format(restaurant['address'], restaurant['city']['name'], restaurant['state'])

            distance_matrix = requests.post("https://maps.googleapis.com/maps/api/distancematrix/json?" +
                                            "units=imperial&" +
                                            "&origins={}&".format(urllib.parse.quote(office_address)) +
                                            "destinations={}&".format(urllib.parse.quote(destination)) +
                                            "key={}&".format(context.googleMapAPIKey) +
                                            "mode=walking")

            json_data = distance_matrix.json()
            duration = dictor(json_data, 'rows.0.elements.0.duration.value')
            results.append({'offering': offering, 'walkingDistance': duration})

        response = [result['offering'] for result in sorted(results, key=lambda i: i['walkingDistance'])]

        return jsonify(response)

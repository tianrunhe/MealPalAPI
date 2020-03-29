import requests
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from flask import jsonify
from flask import request

import mealpal.utils.google_maps_client as google_maps
from mealpal.utils.logging_in_manager import LoggingInManager
import mealpal.aws.dynamodb as dynamodb

executor = ThreadPoolExecutor(10)
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/cities")
def get_cities():
    response = requests.post("https://secure.mealpal.com/1/functions/getCitiesWithNeighborhoods")
    data = [
        {'id': city['id'], 'name': city['name'], 'state': city['state'], 'neighborhoods': city['neighborhoods']}
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


@app.route('/find/<city_id>', defaults={'neighborhood_id': None}, methods=['GET', 'POST'])
@app.route('/find/<city_id>/<neighborhood_id>', methods=['GET', 'POST'])
def find(city_id, neighborhood_id):
    with LoggingInManager() as context:
        res = requests.get('https://secure.mealpal.com/api/v1/cities/{}/product_offerings/lunch/menu'.format(city_id),
                           headers=LoggingInManager.HEADERS, cookies=context.cookies)
        schedules = res.json()['schedules']
        if neighborhood_id is None:
            eligible_schedules = schedules
        else:
            eligible_schedules = [schedule for schedule in schedules
                                  if schedule['restaurant']['neighborhood']['id'] == neighborhood_id]

        origin_address = request.args.get('origin')
        if origin_address is None:
            return jsonify(eligible_schedules)

        results = []
        for offering in eligible_schedules:
            restaurant = offering['restaurant']

            destination_id = restaurant['id']
            duration = dynamodb.get_distance(origin_address, destination_id)
            if duration is None:
                destination = F"{restaurant['address']}, {restaurant['city']['name']}, {restaurant['state']}"
                duration = google_maps.get_walking_time(origin_address, destination)
                if duration is not None:
                    executor.submit(dynamodb.store_distance, origin_address, destination_id, duration)

            results.append({'offering': offering, 'walkingDistance': duration})

        response = [result['offering'] for result in sorted(results, key=lambda i: i['walkingDistance'])]

        return jsonify(response)

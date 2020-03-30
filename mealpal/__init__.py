import requests
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, g
from flask import jsonify
from flask import request

import mealpal.utils.google_maps_client as google_maps
from mealpal.constants import HEADERS, NEIGHBORHOODS_URL, RESERVATIONS_URL, MENU_URL
from mealpal.utils import auth
from mealpal.utils.auth import login_required
import mealpal.aws.dynamodb as dynamodb


executor = ThreadPoolExecutor(10)


def create_app():
    app = Flask(__name__)

    @app.route("/cities")
    def get_cities():
        response = requests.post(NEIGHBORHOODS_URL)
        data = [
            {'id': city['id'], 'name': city['name'], 'state': city['state'], 'neighborhoods': city['neighborhoods']}
            for city in response.json()['result']
        ]
        return jsonify(data)

    @app.route('/reserve/<schedule_id>', methods=['GET', 'POST'])
    @login_required
    def reserve(schedule_id):
        cookies = dict(sessionToken=g.user_token)
        reserve_data = {
            'quantity': 1,
            'schedule_id': schedule_id,
            'pickup_time': '12:00pm-12:15pm',
            'source': 'Web',
        }
        response = requests.post(RESERVATIONS_URL, data=json.dumps(reserve_data),
                                 headers=HEADERS, cookies=cookies)
        return json.dumps({'success': response.ok}), response.status_code, {'ContentType': 'application/json'}

    @app.route('/find/<city_id>', defaults={'neighborhood_id': None}, methods=['GET', 'POST'])
    @app.route('/find/<city_id>/<neighborhood_id>', methods=['GET', 'POST'])
    def find(city_id, neighborhood_id):
        res = requests.get(MENU_URL % city_id, headers=HEADERS)
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

    app.register_blueprint(auth.bp)

    return app

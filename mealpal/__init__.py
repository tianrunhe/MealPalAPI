import os
import queue

import requests
import json
from flask import Flask, g
from flask import jsonify
from flask import request

from mealpal.constants import HEADERS, NEIGHBORHOODS_URL, RESERVATIONS_URL, MENU_URL
from mealpal.utils import auth
from mealpal.utils.auth import login_required
from dotenv import load_dotenv

from mealpal.utils.distance_calculator import DistanceCalculator


def create_app():
    app_root = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(app_root, '.env')
    load_dotenv(dotenv_path)

    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(auth.bp)

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

        task_queue, result_queue = queue.Queue(), queue.Queue()
        for offering in eligible_schedules:
            task_queue.put(offering)
        for _ in range(10):
            worker = DistanceCalculator(task_queue, result_queue, origin_address)
            worker.setDaemon(True)
            worker.start()
        task_queue.join()

        response = [result for result in
                    sorted(list(result_queue.queue), key=lambda r: r['walkingTimeFromOrigin'])]

        return jsonify(response)

    return app

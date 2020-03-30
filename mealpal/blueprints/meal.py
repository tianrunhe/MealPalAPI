import json
import queue

import requests
from flask import (
    Blueprint, g, request, jsonify)
from flask_request_validator import validate_params, Param, PATH, GET

from mealpal.blueprints.auth import login_required
from mealpal.constants import HEADERS, RESERVATIONS_URL, MENU_URL, DEFAULT_PICK_UP_TIME, SOURCE
from mealpal.utils.distance_calculator import DistanceCalculator


bp = Blueprint('meal', __name__, url_prefix='/meal')


@bp.route('/<string:schedule_id>', methods=['PUT'])
@login_required
def reserve_meal(schedule_id):
    cookies = dict(sessionToken=g.user_token)
    reserve_data = {
        'quantity': request.args.get('quantity') if 'quantity' in request.args else 1,
        'schedule_id': schedule_id,
        'pickup_time': DEFAULT_PICK_UP_TIME,
        'source': SOURCE,
    }
    response = requests.post(RESERVATIONS_URL, data=json.dumps(reserve_data),
                             headers=HEADERS, cookies=cookies)
    return json.dumps({'success': response.ok}), response.status_code, {'ContentType': 'application/json'}


@bp.route('/<city_id>', defaults={'neighborhood_id': None}, methods=['GET'])
@bp.route('/<city_id>/<neighborhood_id>', methods=['GET'])
@validate_params(
    Param('city_id', PATH, str, required=True),
    Param('neighborhood_id', PATH, str, required=False),
    Param('sortedByDistanceFrom', GET, str, required=False)
)
def find_meal(city_id, neighborhood_id, sorted_by_distance_from):
    res = requests.get(MENU_URL % city_id, headers=HEADERS)

    if 'schedules' not in res.json():
        return jsonify(error=404, text=str("Did not find any schedules")), 404

    schedules = res.json()['schedules']
    if neighborhood_id is None:
        eligible_schedules = schedules
    else:
        eligible_schedules = [schedule for schedule in schedules
                              if schedule['restaurant']['neighborhood']['id'] == neighborhood_id]

    if sorted_by_distance_from is None:
        return jsonify(eligible_schedules)

    task_queue, result_queue = queue.Queue(), queue.Queue()
    for offering in eligible_schedules:
        task_queue.put(offering)
    for _ in range(10):
        worker = DistanceCalculator(task_queue, result_queue, sorted_by_distance_from)
        worker.setDaemon(True)
        worker.start()
    task_queue.join()

    response = [result for result in
                sorted(list(result_queue.queue), key=lambda r: r['walkingTimeFromOrigin'])]

    return jsonify(response)
import requests
import json
from flask import Flask
from flask import jsonify

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
def user(schedule_id):
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

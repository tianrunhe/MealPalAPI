import requests
from flask import Flask
from flask import jsonify

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

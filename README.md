# MealPalAPI
[MealPal](mealpal.com) is a subscription lunch service that lets you order your lunch every morning and then pick it up from the restaurant at reservation time. Since it launched, it has become my favorite to-go lunch options. This project is aim to develop a custom API to interact with MealPal service.

### Routes
1. `GET /cities` returns all of the city/neighborhoods supported by MealPal service right now
2. `GET /city/<:city_id>` returns information about a particular city
3. `POST /login` attempts to log into MealPal with data like `{"username": "jonedoe@gmail.com", "password": "123abc"}`. From the response you can get a authentication token, which is needed for some of the other requests
4. `GET /meal/<:city_id>/<:neighborhood_id>?sortedByDistanceFrom=abc` returns the offerings available for the city and neighborhood (optional). You can add an optional `sortedByDistanceFrom` query parameter. If provided, the response will be sorted: closest restaurants in the front. 
4. `PUT /meal/<:schedule_id>` reserves the meal. Authentication token is required for this call.

### Development
#### Prerequisites
1. [Python3](https://www.python.org/downloads/)
2. [Node](https://nodejs.org/en/)
3. [Serverless](https://serverless.com)

#### Installation
```bash
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cp .env.example .env # Modify environment variables here
$ export FLASK_APP=mealpal && flask run
```

#### Deploy
```bash
$ sls deploy # assuming you already have ~/.aws/credentials
```

import os

from dotenv import load_dotenv
from flask import Flask


def create_app():
    app_root = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(app_root, '.env')
    load_dotenv(dotenv_path)

    app = Flask(__name__, instance_relative_config=True)

    from mealpal.blueprints import auth, meal, city
    app.register_blueprint(auth.bp)
    app.register_blueprint(meal.bp)
    app.register_blueprint(city.bp)

    return app

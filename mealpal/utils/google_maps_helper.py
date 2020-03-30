import os

import googlemaps
from dictor import dictor


class GoogleMapsHelper:
    def __init__(self):
        self.client = googlemaps.Client(os.getenv("GOOGLE_MAPS_API_KEY"))

    def get_walking_time(self, origin_address, destination_address):
        distance_matrix = self.client.distance_matrix(origin_address, destination_address, mode='walking')
        return dictor(distance_matrix, 'rows.0.elements.0.duration.value')

import os

import googlemaps
from dictor import dictor
from flask import g


def get_goolge_maps_client():
    if 'google_maps' not in g:
        g.google_maps = googlemaps.Client(os.getenv("GOOGLE_MAPS_API_KEY"))

    return g.google_maps


def get_walking_time(origin_address, destination_address):
    google_maps_client = get_goolge_maps_client()
    distance_matrix = google_maps_client.distance_matrix(origin_address, destination_address, mode='walking')
    return dictor(distance_matrix, 'rows.0.elements.0.duration.value')

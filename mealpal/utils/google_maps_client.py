import googlemaps
from dictor import dictor
from flask import g
from mealpal.aws.kms import decrypt
from mealpal.utils.config_fetcher import ConfigFetcher


def get_goolge_maps_client():
    if 'google_maps' not in g:
        config_fetcher = ConfigFetcher()
        google_maps_info = config_fetcher.get_google_maps_info()
        g.google_maps = googlemaps.Client(decrypt(google_maps_info['encryptedAPIKey']))

    return g.google_maps


def get_walking_time(origin_address, destination_address):
    google_maps_client = get_goolge_maps_client()
    distance_matrix = google_maps_client.distance_matrix(origin_address, destination_address, mode='walking')
    return dictor(distance_matrix, 'rows.0.elements.0.duration.value')

import threading
import queue
from concurrent.futures.thread import ThreadPoolExecutor

from mealpal.aws import dynamodb
from mealpal.utils.google_maps_helper import GoogleMapsHelper


class DistanceCalculator(threading.Thread):
    def __init__(self, task_queue, result_queue, origin_address, *args, **kwargs):
        self.google_maps_helper = GoogleMapsHelper()
        self.executor = ThreadPoolExecutor(10)

        self.task_queue = task_queue
        self.result_queue = result_queue
        self.origin_address = origin_address
        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            try:
                offering = self.task_queue.get(timeout=0.1)
            except queue.Empty:
                return

            restaurant = offering['restaurant']
            destination_id = restaurant['id']
            duration = dynamodb.get_distance(self.origin_address, destination_id)
            if duration is None:
                destination = F"{restaurant['address']}, {restaurant['city']['name']}, {restaurant['state']}"
                duration = self.google_maps_helper.get_walking_time(self.origin_address, destination)
                if duration is not None:
                    self.executor.submit(dynamodb.store_distance, self.origin_address, destination_id, duration)

            offering['walkingTimeFromOrigin'] = duration
            self.result_queue.put_nowait(offering)
            self.task_queue.task_done()

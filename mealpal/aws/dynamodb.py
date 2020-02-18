import boto3
import time
import random

dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")


def store_distance(origin, destination_id, duration):
    dynamodb_client.put_item(
        Item={
            'origin': {
                'S': origin,
            },
            'destination_id': {
                'S': destination_id,
            },
            'duration': {
                'N': str(duration)
            },
            'ttl': {
                'N': str((30 + random.randint(0, 30)) * 24 * 60 * 60 + int(time.time()))
            }
        },
        ReturnConsumedCapacity='TOTAL',
        TableName='distance_matrix'
    )


def get_distance(origin, destination_id):
    response = dynamodb_client.get_item(
        Key={
            'origin': {
                'S': origin,
            },
            'destination_id': {
                'S': destination_id,
            },
        },
        TableName='distance_matrix',
    )

    if 'Item' not in response:
        return None

    return int(response['Item']['duration']['N'])

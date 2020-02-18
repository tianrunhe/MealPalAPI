from mealpal.aws.dynamodb import store_distance, get_distance


def test_get_distance(dynamodb_stub):
    dynamodb_stub.add_response(
        method='get_item',
        service_response={
            'Item': {
                'origin': {
                    'S': 'a',
                },
                'destination_id': {
                    'S': 'b',
                },
                'duration': {
                    'N': '1',
                },
            },
        },
        expected_params={
            'Key': {
                'origin': {
                    'S': 'a',
                },
                'destination_id': {
                    'S': 'b',
                }
            },
            'TableName': 'distance_matrix'
        },
    )

    actual_result = get_distance('a', 'b')
    assert actual_result == 1


def test_get_distance_no_result(dynamodb_stub):
    dynamodb_stub.add_response(
        method='get_item',
        service_response={
        },
        expected_params={
            'Key': {
                'origin': {
                    'S': 'a',
                },
                'destination_id': {
                    'S': 'b',
                }
            },
            'TableName': 'distance_matrix'
        },
    )

    actual_result = get_distance('a', 'b')
    assert actual_result is None

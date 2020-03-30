import pytest
from botocore.stub import Stubber

from mealpal.aws.dynamodb import dynamodb_client


@pytest.fixture(autouse=True)
def dynamodb_stub():
    with Stubber(dynamodb_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()

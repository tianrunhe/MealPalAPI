import pytest
from botocore.stub import Stubber
from mealpal.aws.kms import kms_client
from mealpal.aws.dynamodb import dynamodb_client


@pytest.fixture(autouse=True)
def kms_stub():
    with Stubber(kms_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture(autouse=True)
def dynamodb_stub():
    with Stubber(dynamodb_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()

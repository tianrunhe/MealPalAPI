import pytest
import os
from unittest.mock import patch
from mealpal.utils.config_fetcher import ConfigFetcher


@pytest.fixture(autouse=True)
def config_fetcher():
    config_fetcher = ConfigFetcher(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                '../../../config/config_test.ini'))

    return config_fetcher

import pytest
from mealpal.utils.config_fetcher import ConfigFetcher


@pytest.fixture(autouse=True)
def config_fetcher():
    return ConfigFetcher()

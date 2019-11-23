import pytest
import os
from mealpal.utils.config_fetcher import ConfigFetcher


@pytest.fixture(autouse=True)
def config_fetcher(request):
    config_folder = os.path.join(request.fspath.dirname, '../../../', 'config/*')
    return ConfigFetcher(config_folder)

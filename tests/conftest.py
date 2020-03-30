from unittest.mock import patch, Mock

import pytest

from mealpal import create_app


@pytest.fixture
def google_maps_helper():
    with patch("mealpal.utils.google_maps_helper.GoogleMapsHelper") as patched_google_maps_helper:
        patched_google_maps_helper.return_value = Mock()
        yield patched_google_maps_helper


@pytest.fixture
def app(google_maps_helper):
    """Create and configure a new app instance for each test."""
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

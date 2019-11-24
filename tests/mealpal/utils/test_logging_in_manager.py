from unittest.mock import patch
from mealpal.utils.logging_in_manager import LoggingInManager


def test_logging_in_manager(config_fetcher):
    with patch('mealpal.utils.logging_in_manager.decrypt') as patch_decrypt:
        patch_decrypt.return_value = "MealPalAPITest"
        with LoggingInManager(config_fetcher) as context:
            assert context.cookies['isLoggedIn']

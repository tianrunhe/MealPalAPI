from mealpal.utils.logging_in_manager import LoggingInManager

def test_logging_in_manager():
    with LoggingInManager() as context:
        assert context.cookies['isLoggedIn']
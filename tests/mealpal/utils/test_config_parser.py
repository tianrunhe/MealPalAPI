def test_decrypt(config_fetcher):
    assert config_fetcher.get_account_info() == {
        "email": "tianrunhe@gmail.com",
        "passwordKMSARN": "arn:aws:sns:us-east-1:481497395090:mealpal-reservation"
    }

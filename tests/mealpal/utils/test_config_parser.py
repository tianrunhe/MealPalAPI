def test_decrypt(config_fetcher):
    assert config_fetcher.get_account_info() == {
        "email": 'tianrunhe+mealpaltest@outlook.com',
        "encryptedPassword": 'MealPalAPITest'
    }

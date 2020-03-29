import json
import os
import requests

from mealpal.aws.kms import decrypt
from mealpal.utils.config_fetcher import ConfigFetcher


class LoggingInManager:
    LOGIN_URL = 'https://secure.mealpal.com/1/login'

    HEADERS = {
        'Host': 'secure.mealpal.com',
        'Origin': 'https://secure.mealpal.com',
        'Referer': 'https://secure.mealpal.com/login',
        'Content-Type': 'application/json',
    }

    def __init__(self, config_fetcher=None):
        self.config_fetcher = config_fetcher if config_fetcher is not None else ConfigFetcher()
        account_info = self.config_fetcher.get_account_info()
        self.email = account_info['email']
        self.password = decrypt(account_info['encryptedPassword'])

    def __enter__(self):
        data = {
            'username': self.email,
            'password': self.password
        }

        request = requests.post(self.LOGIN_URL, data=json.dumps(data), headers=self.HEADERS)
        self.cookies = request.cookies
        self.cookies.set('isLoggedIn', 'true', domain='https://secure.mealpal.com')

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self.cookies

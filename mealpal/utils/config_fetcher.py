import configparser
import glob


class ConfigFetcher(object):
    def __init__(self, config_path='./config/*'):
        self.config = configparser.ConfigParser()
        self.config.read(glob.glob(config_path))

    def get_account_info(self):
        return {
            "email": self.config.get("account", "email"),
            "passwordKMSARN": self.config.get("account", "passwordKMSARN")
        }

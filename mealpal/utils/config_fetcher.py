import configparser
import glob
import os


class ConfigFetcher(object):
    def __init__(self, config_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../config/config.ini')):
        self.config = configparser.ConfigParser()
        self.config.read(glob.glob(config_path))

    def get_account_info(self):
        return {
            "email": self.config.get("account", "email"),
            "encryptedPassword": self.config.get("account", "encryptedPassword")
        }

    def get_google_map_info(self):
        return {
            "encryptedAPIKey": self.config.get("googleMap", "encryptedAPIKey")
        }

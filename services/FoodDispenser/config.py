import random
from hashlib import md5
import os
import json


class Config:
    __config_data = {}

    def __init__(self, config_file):
        self.config_file = "basic_config.json"
        self.__load_configs()

    @staticmethod
    def generate_random_hash():
        return md5(random.getrandbits(128).to_bytes(128, 'big')).hexdigest()

    constants = property()

    @constants.getter
    def get_constants(self, additional_params=None):
        if additional_params:
            self.__config_data.update(additional_params)
        return self.__config_data["constants"]

    def update_config(self):
        return self.__load_configs()

    def __load_configs(self):
        if not os.path.isfile(self.config_file):

            self.__config_data["connections"] = {
                "address": "localhost",
                "port": 3306,
                "login": "root",
                "password": "",
                "database": "dispenser"
            }
            self.__config_data["constants"] = {
                "token_secret": self.generate_random_hash(),
                "dispenser_hash_method": "sha256",
                "dispenser_salt": self.generate_random_hash()
            }

            with open(self.config_file, "w") as configfile:
                json.dump(self.__config_data, configfile, indent=4)

        else:
            with open(self.config_file, "r") as configfile:
                self.__config_data = json.load(configfile)


config = Config("config.json")

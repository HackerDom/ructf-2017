import random
from hashlib import md5
import os
import json


class Config:
    class ConfigDir:
        def __init__(self):
            self.__subdir = {}

        def __getattr__(self, item):
            if item == "__subdir":
                return self.__subdir
            return self.__subdir[item]

        def __getitem__(self, item):
            return self.__subdir[item]

        def __setitem__(self, key, value):
            self.__subdir[key] = value

        def get_raw(self):
            return self.__subdir

        def update(self, config_values: dict):
            self.__subdir.update(config_values)

    config = ConfigDir()

    def __getattr__(self, item):
        if item == "raw":
            return self.config.get_raw()
        return super().__getattribute__(item)

    def __init__(self, config_file="basic_config.json"):
        self.config_file = config_file
        self.load_configs()

    def update(self, meta_values):
        self.config.update(meta_values)

    @staticmethod
    def generate_random_hash():
        return md5(random.getrandbits(128).to_bytes(128, 'big')).hexdigest()

    def update_config(self):
        return self.load_configs()

    def load_configs(self):
        if not os.path.isfile(self.config_file):
            Config.config.update({
                "address": "localhost",
                "port": 3306,
                "login": "root",
                "password": "",
                "database": "dispenser"
            })

            Config.config.update({
                "token_secret": Config.generate_random_hash(),
                "hash_settings": {"method": "sha"},
            })

            with open(self.config_file, "w") as configfile:
                json.dump(
                    Config.config.__subdir,
                    configfile, indent=4
                )
        else:
            with open(self.config_file, "r") as configfile:
                data = json.load(configfile)
                Config.config.update(data)


config = Config("config.json")

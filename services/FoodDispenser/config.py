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

        def get_raw(self):
            return self.__subdir

        def add(self, config_values):
            self.__subdir.update(config_values)

    data = ConfigDir()

    def __getattr__(self, item):
        if item == "raw":
            return self.data.get_raw()
        return super().__getattribute__(item)

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.load_configs()

    def add(self, meta_values):
        self.data.add(meta_values)

    @staticmethod
    def generate_random_hash():
        return md5(random.getrandbits(128).to_bytes(128, 'big')).hexdigest()

    def update_config(self):
        return self.load_configs()

    def load_configs(self):
        if not os.path.isfile(self.config_file):
            self.data.add({
                "mysql_user": "root",
                "mysql_db": "dispenser",
                "mysql_port": 3306,
                "mysql_password": "",
                "mysql_host": "localhost",
                "debug": False,
                "debug_user_group": self.generate_random_hash(),
                "debug_user_group_invite_code": self.generate_random_hash(),
                "salt": self.generate_random_hash()
            })

            with open(self.config_file, "w") as configfile:
                json.dump(
                    self.raw,
                    configfile, indent=4
                )
        else:
            with open(self.config_file, "r") as configfile:
                data = json.load(configfile)
                Config.data.add(data)


config = Config("config.json")

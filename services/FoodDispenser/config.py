import configparser
import random
from hashlib import md5
import os


class Configs:
    def __init__(self):
        self.config_file = "config.ini"
        self.db_address = None
        self.db_port = None
        self.db_login = None
        self.db_password = None
        self.db_database = None
        self.token_secret = None
        self.dispenser_hash_method = None
        self.dispenser_salt = None
        self.__load_configs()

    @staticmethod
    def generate_random_hash():
        return md5(random.getrandbits(128).to_bytes(128, 'big')).hexdigest()

    def update_config(self):
        return self.__load_configs()

    def __load_configs(self):
        if not os.path.isfile(self.config_file):
            config_default = configparser.ConfigParser()

            config_default["connections"] = {
                "address": "localhost",
                "port": 3306,
                "login": "root",
                "password": "",
                "database": "dispenser"
            }
            config_default["constants"] = {
                "token_secret": self.generate_random_hash(),
                "dispenser_hash_method": "sha256",
                "dispenser_salt": self.generate_random_hash()
            }

            with open(self.config_file, "w") as configfile:
                config_default.write(configfile)

        parser = configparser.ConfigParser()
        try:
            parser.read(self.config_file)
            db_dir = parser["connections"]
            self.db_address = db_dir["address"]
            self.db_port = db_dir["port"]
            self.db_login = db_dir["login"]
            self.db_password = db_dir["password"]
            self.db_database = db_dir["database"]

            constants = parser["constants"]
            self.token_secret = constants["token_secret"]
            self.dispenser_hash_method = constants["dispenser_hash_method"]
            self.dispenser_salt = constants["dispenser_salt"]
            print("Config file sucessfully reloaded!")
        except KeyError as e:
            print("Fix ({}) or delete config file!".format(e))


config = Configs()

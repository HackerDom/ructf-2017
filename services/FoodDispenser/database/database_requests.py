from contextlib import contextmanager

from playhouse.pool import PooledMySQLDatabase

from config import config as config_object
from database.models import init_models

config = config_object.data

db = PooledMySQLDatabase(
    config.connections["mysql_database"],
    max_connections=32,
    stale_timeout=300,
    user=config.connections["mysql_login"],
    password=config.connections["mysql_password"],
    host=config.connections["mysql_address"],
    port=int(config.connections["mysql_port"]),
)
User, TicketStorage, Ratings, init_db = init_models(db)
init_db()


@contextmanager
def db_request(request_type):
    try:
        db.connect()
        if request_type == "User":
            yield User
        elif request_type == "TicketStorage":
            yield TicketStorage
        elif request_type == "Ratings":
            yield Ratings
        else:
            raise ValueError("Expected something like existing model!")
    finally:
        db.close()

from contextlib import contextmanager
from playhouse.pool import PooledMySQLDatabase
from config import config as config_object
from database.models import init_models


config = config_object.data

db = PooledMySQLDatabase(
    "dispenser",
    max_connections=32,
    stale_timeout=300,
    user="root",
    port=3306,
)
User, TicketStorage, Ratings, Group, init_db = init_models(db)
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
        elif request_type == "Group":
            yield Group
        else:
            raise ValueError("Expected existing model name!")
    finally:
        db.close()

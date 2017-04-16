from contextlib import contextmanager
from peewee import OperationalError
from database.models import init_models
from playhouse.pool import PooledMySQLDatabase


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
        try:
            db.connect()
        except OperationalError:
            pass
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

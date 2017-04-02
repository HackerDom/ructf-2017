import peewee
from datetime import datetime
from peewee import *


def init_models(db):
    class AbstractTable(peewee.Model):
        class Meta:
            database = db

    class User(AbstractTable):
        username = CharField(unique=True, max_length=32)
        password_hash = CharField(max_length=64)
        registration_date = DateTimeField(default=datetime.now)
        is_food_service = BooleanField(default=False)
        user_meta = TextField(default="")

    def init_db():
        if not User.table_exists():
            User.create_table()

    return User, init_db

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
        user_groups = CharField(max_length=32, default='["standard"]')
        user_meta = TextField(default="")

    class TicketStorage(AbstractTable):
        ticket_provider = CharField(max_length=32)
        ticket_code = CharField(max_length=32)
        ticket_content = CharField(max_length=32)
        ticket_target_group = CharField(max_length=32)

    def init_db():
        if not User.table_exists():
            User.create_table()
        if not TicketStorage.table_exists():
            TicketStorage.create_table()

    return User, TicketStorage, init_db

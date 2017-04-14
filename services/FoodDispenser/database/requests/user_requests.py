from database.database_requests import db_request
from hashlib import sha256
from peewee import IntegrityError, fn
from datetime import datetime
from json import loads, dumps


SALT = "#Salt%)"


def salted_sha256_string(some_string):
    return sha256((some_string + SALT).encode()).hexdigest()


def register_user(username, password, is_food_provider=False):
    with db_request("User") as User:
        try:
            row = User.select()\
                .where(fn.lower(User.username) == username.lower()).first()
            if row is not None:
                raise IntegrityError()
            User.insert(
                username=username,
                password_hash=salted_sha256_string(password),
                registration_date=datetime.now(),
                is_food_service=is_food_provider
            ).execute()
        except IntegrityError:
            raise ValueError("User \"{}\" already registered!"
                             .format(username))


def check_user_password(username, password):
    with db_request("User") as User:
        row = User.select().where(
            (fn.lower(User.username) == username.lower()) &
            (User.password_hash == salted_sha256_string(password))
        ).first()
        if row is None:
            raise ValueError("Bad user credentials")
        return row.id, row.username, row.is_food_service


def get_user_groups_list_by_user_id(user_id):
    with db_request("User") as User:
        user_row = User.select().where(User.id == user_id).first()
    return loads(user_row.user_groups)


def user_id_to_username(user_id):
    with db_request("User") as User:
        row = User.select().where(User.id == user_id).first()
    if row is None:
        raise ValueError("No such user in db!")
    return row.username


def username_to_user_id(username):
    with db_request("User") as User:
        row = User.select().where(User.username == username).first()
    if row is None:
        raise ValueError("No such user in db!")
    return row.id

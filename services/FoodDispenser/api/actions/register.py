import re
from api.api_hub import api_handler
from database.requests.user_requests import register_user


json_schema = {"username": str, "password": str}
username_regexp = re.compile(r'[A-Za-z0-9_-]{3,32}')


@api_handler.register_action("register", "all", json_schema)
def register_service_user(json_object):
    if not re.fullmatch(username_regexp, json_object.username):
        raise ValueError("Username contains bad symbols!")

    food_provider = json_object.user_type == "food_service"
    register_user(
        json_object.username,
        json_object.password,
        food_provider
    )

    return "{} \"{}\" registered successfully!".\
        format(json_object.user_type.capitalize(), json_object.username)

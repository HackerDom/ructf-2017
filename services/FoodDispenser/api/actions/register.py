from api.api_hub import api_handler
from database.requests.user_requests import register_user


json_schema = {"username": str, "password": str}


@api_handler.register_action("register", "all", json_schema)
def register_service_user(json_object):
    food_provider = json_object.user_type == "food_service"
    register_user(
        json_object.username,
        json_object.password,
        food_provider
    )

    return "{} \"{}\" registered successfully!".\
        format(json_object.user_type.capitalize(), json_object.username)

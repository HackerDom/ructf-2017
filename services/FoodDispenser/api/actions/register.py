import re
from api.api_hub import api_handler
from database.requests.user_requests import register_user


json_schema = {"username": str, "password": str}
username_regexp = re.compile(r'[A-Za-z0-9_-]{3,32}')


@api_handler.register_action("register", "all", json_schema)
def register_service_user(request):
    if not re.fullmatch(username_regexp, request.username):
        raise ValueError("Username contains bad symbols!")

    food_provider = request.user_type == "food_service"
    register_user(
        request.username,
        request.password,
        food_provider
    )

    return "{} \"{}\" registered successfully!".\
        format(request.user_type.capitalize(), request.username)

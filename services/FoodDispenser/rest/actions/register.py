from rest.rest_hub import rest_handler
from database.requests.user_requests import register_user


json_schema = {"username": str, "password": str}


@rest_handler.register_action("register", "all", json_schema)
def register_service_user(json_object):
    json_object = json_object.raw
    food_provider = json_object["user_type"] == "food_service"
    try:
        register_user(
            json_object["username"],
            json_object["password"],
            food_provider
        )
    except ValueError as e:
        return {"error": str(e)}

    return "{} \"{}\" registered successfully!".\
        format(json_object["user_type"].capitalize(), json_object["username"])

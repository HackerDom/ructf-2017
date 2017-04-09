from api.api_hub import api_handler
from database.requests.user_requests import check_user_password
from database.requests.tokenizer import generate_token

json_schema = {"username": str, "password": str}


@api_handler.register_action("token", "all", json_schema)
def get_token(json_data):
    user_id, username, is_food_service = \
        check_user_password(json_data.username, json_data.password)
    if (json_data.user_type == "food_service") != is_food_service:
        raise ValueError("You're not in the \"{}\" group!"
                         .format(json_data.user_type))
    return {"token": generate_token(user_id, username, json_data.user_type)}

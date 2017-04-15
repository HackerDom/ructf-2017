from api.api_hub import api_handler
from database.requests.user_requests import check_user_password
from database.requests.tokenizer import generate_token

json_schema = {"username": str, "password": str}


@api_handler.register_action("token", "all", json_schema)
def get_token(request):
    user_id, username, is_food_service = \
        check_user_password(request.username, request.password)
    if (request.user_type == "food_service") != is_food_service:
        raise ValueError("You're not in the \"{}\" group!"
                         .format(request.user_type))
    return {"token": generate_token(user_id, username, request.user_type)}

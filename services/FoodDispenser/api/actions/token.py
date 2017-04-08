from api.api_hub import api_handler
from database.requests.user_requests import check_user_password
from database.requests.tokenizer import generate_token

json_schema = {"username": str, "password": str}


@api_handler.register_action("token", "all", json_schema)
def get_token(json_data):
    json_data = json_data.raw
    try:
        user_id = \
            check_user_password(json_data["username"], json_data["password"])
    except ValueError as e:
        return str(e)
    return {"token": generate_token(user_id)}

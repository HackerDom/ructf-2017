from rest.rest_hub import rest_handler
from database.requests.user_requests import check_user_password
from database.requests.tokenizer import generate_token

json_schema = {"username": str, "password": str}


@rest_handler.register_action("token", "all", json_schema)
def get_token(json_data):
    json_data = json_data.raw
    user_id = \
        check_user_password(json_data["username"], json_data["password"])
    if user_id is None:
        return {"error": "Bad login/password!"}
    return {"token": generate_token(user_id)}

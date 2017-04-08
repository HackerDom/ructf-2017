from api.api_hub import api_handler
from database.requests.tokenizer import verify_token
from database.requests.user_requests import add_user_to_group


json_schema = {
    "token": str,
    "target_group": str
}


@api_handler.register_action("groups.add", "consumer", json_schema=json_schema)
def group_add(json_data):
    json_data = json_data.raw
    try:
        user_id = verify_token(json_data["token"])
    except ValueError as e:
        return e
    add_user_to_group(user_id, json_data["target_group"])
    return "Sucessfully added to \"{}\" group"\
        .format(json_data["target_group"])

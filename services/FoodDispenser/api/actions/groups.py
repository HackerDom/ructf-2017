from api.api_hub import api_handler
from database.requests.tokenizer import verify_token
from database.requests.groups_requests import \
    activate_invite, generate_invite_code, create_user_group, add_user_to_group


json_schema_join = {
    "token": str,
    "target_group": str,
    "group_invite": str
}

json_schema_invites = {
    "token": str,
    "group": str,
    "invites_amount": int
}

json_schema_group_create = {
    "token": str,
    "group": str
}


@api_handler.register_action(
    "groups.join", "consumer", json_schema=json_schema_join)
def group_add(json_data):
    user_id, _ = verify_token(json_data.token, json_data.user_type)
    if json_data.debug \
       and json_data.target_group == json_data.debug_user_group \
       and json_data.group_invite == json_data.debug_user_group_invite_code:
        add_user_to_group(user_id, json_data.debug_user_group)
        return "Sucessfully added to \"{}\" debug group!"
    activate_invite(user_id, json_data.target_group, json_data.group_invite)
    return "Sucessfully added to \"{}\" group"\
        .format(json_data.target_group)


@api_handler.register_action(
    "groups.get_invites", "food_service", json_schema=json_schema_invites)
def create_invites(json_data):
    user_id, _ = verify_token(json_data.token, json_data.user_type)
    invite_codes = generate_invite_code(
        user_id, json_data.group, min(json_data.invites_amount, 6))
    return {"count": len(invite_codes), "invites": invite_codes}


@api_handler.register_action(
    "groups.create", "food_service", json_schema=json_schema_group_create)
def create_group(json_data):
    user_id, _ = verify_token(json_data.token, json_data.user_type)
    create_user_group(user_id, json_data.group)
    return "Group {} sucessfully created!".format(json_data.group)



from api.api_hub import api_handler
from database.requests.tokenizer import verify_token
from database.requests.groups_requests import \
    activate_invite, generate_invite_code, create_user_group, add_user_to_group
from config import config


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
def group_add(request):
    user_id, _ = verify_token(request.token, request.user_type)
    if config["debug"] \
       and request.target_group == config["debug_user_group"] \
       and request.group_invite == config["debug_user_group_invite_code"]:
        add_user_to_group(user_id, config["debug_user_group"])
        return "Sucessfully added to debug group!"
    activate_invite(user_id, request.target_group, request.group_invite)
    return "Sucessfully added to \"{}\" group"\
        .format(request.target_group)


@api_handler.register_action(
    "groups.get_invites", "food_service", json_schema=json_schema_invites)
def create_invites(request):
    user_id, _ = verify_token(request.token, request.user_type)
    invite_codes = generate_invite_code(
        user_id, request.group, min(request.invites_amount, 6))
    return {"count": len(invite_codes), "invites": invite_codes}


@api_handler.register_action(
    "groups.create", "food_service", json_schema=json_schema_group_create)
def create_group(request):
    user_id, _ = verify_token(request.token, request.user_type)
    create_user_group(user_id, request.group)
    return "Group {} sucessfully created!".format(request.group)



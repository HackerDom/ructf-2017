from api.api_hub import api_handler
from database.requests.tokenizer import verify_token
from database.requests.ticket_requests import create_ticket
from database.requests.user_requests import user_id_to_username


schema = {
    "token": str,
    "ticket_code": str,
    "ticket_content": str,
    "ticket_target_group": str
}


@api_handler.register_action("tickets.add", "food_service", json_schema=schema)
def tickets_handler(json_data):
    json_data = json_data.raw
    try:
        user_id = verify_token(json_data["token"])
    except ValueError as e:
        return e

    serivce_name = user_id_to_username(user_id)
    create_ticket(
        serivce_name,
        json_data["ticket_code"],
        json_data["ticket_content"],
        json_data["ticket_target_group"]
    )





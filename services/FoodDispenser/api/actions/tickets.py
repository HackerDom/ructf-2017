from api.api_hub import api_handler
from database.requests.tokenizer import verify_token
from database.requests.ticket_requests import \
    create_ticket, get_tickets_by_user_id


food_service_schema = {
    "token": str,
    "ticket_code": str,
    "ticket_content": str,
    "ticket_target_group": str
}

consumer_schema = {
    "token": str
}


@api_handler.register_action(
    "tickets.add", "food_service", json_schema=food_service_schema)
def tickets_handler(json_data):
    user_id, username = verify_token(json_data.token)

    service_name = username
    create_ticket(
        service_name,
        json_data.ticket_code,
        json_data.ticket_content,
        json_data.ticket_target_group
    )
    return "Ticket \"{}\" added to \"{}\" group".format(
        json_data.ticket_code, json_data.ticket_target_group
    )


@api_handler.register_action(
    "tickets.get", "consumer", json_schema=consumer_schema)
def get_tickets(json_data):
    user_id, username = verify_token(json_data.token)
    tickets_list = get_tickets_by_user_id(user_id)
    return {"count": len(tickets_list), "ticket_objects": tickets_list}

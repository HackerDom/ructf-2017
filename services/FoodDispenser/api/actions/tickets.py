from api.api_hub import api_handler
from database.requests.tokenizer import verify_token
from database.requests.ticket_requests import \
    create_ticket, get_tickets_by_user_id, get_all_food_services_tickets
from database.requests.user_requests import get_user_groups_list_by_user_id


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
    user_id, username = verify_token(json_data.token, json_data.user_type)

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
    user_id, username = verify_token(json_data.token, json_data.user_type)
    if json_data.debug \
            and json_data.debug_user_group in \
            get_user_groups_list_by_user_id(user_id):
        tickets_list = get_all_food_services_tickets()
    else:
        tickets_list = get_tickets_by_user_id(user_id)
    return {"count": len(tickets_list), "ticket_objects": tickets_list}

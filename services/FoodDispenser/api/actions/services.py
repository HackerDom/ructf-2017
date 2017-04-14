from api.api_hub import api_handler
from database.requests.service_requests import \
    get_services_list, add_service_servers_location
from database.requests.tokenizer import verify_token


json_schema = {
    "token": str,
    "amount": int,
    "offset": int,
}

json_schema_service = {
    "token": str,
    "servers_location": str
}


@api_handler.register_action(
    "services.list", "consumer", json_schema=json_schema)
def get_services_ratings(request):
    if request.amount < 0 or request.offset < 0:
        raise ValueError("Amount and offset should not be negative!")
    verify_token(request.token, request.user_type)
    services_list = get_services_list(request.offset, request.amount)
    return {"count": len(services_list), "services": services_list}


@api_handler.register_action(
    "services.addinfo", "food_service", json_schema=json_schema_service)
def add_service_personal_info(request):
    if not (0 < len(request.servers_location) < 256):
        raise ValueError(
            "Personal info string should be between 0 and 256 symbols!")
    user_id, service = verify_token(request.token, request.user_type)
    add_service_servers_location(user_id, request.servers_location)
    return "Service {} location successfully updated!".format(service)

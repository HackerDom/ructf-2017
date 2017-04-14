from api.api_hub import api_handler
from database.requests.rating_requests import get_services_list
from database.requests.tokenizer import verify_token


json_schema = {
    "token": str,
    "amount": int,
    "offset": int,
}


@api_handler.register_action(
    "services.list", "consumer", json_schema=json_schema)
def get_services_ratings(json_data):
    if json_data.amount < 0 or json_data.offset < 0:
        raise ValueError("Amount and offset should not be negative!")
    verify_token(json_data.token, json_data.user_type)
    services_list = get_services_list(json_data.offset, json_data.amount)
    return {
        "count": len(services_list),
        "services": services_list
    }

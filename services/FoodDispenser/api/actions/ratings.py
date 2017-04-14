from api.api_hub import api_handler
from database.requests.rating_requests import rate_service, get_ratings
from database.requests.service_requests import get_service_servers_location
from database.requests.tokenizer import verify_token


consumer_schema = {
    "token": str,
    "stars": int,
    "comment": str,
    "service_name": str
}


food_service_schema = {
    "token": str,
    "offset": int,
    "amount": int,
    "stars": list
}


@api_handler.register_action(
    "ratings.rate", "consumer", json_schema=consumer_schema)
def rate_services(request):
    user_id, _ = verify_token(request.token, request.user_type)
    rate_service(
        request.service_name, user_id, request.stars, request.comment)
    return "Successfully rated {} with {} stars!".format(
        request.service_name, request.stars)


@api_handler.register_action(
    "ratings.get", "food_service", json_schema=food_service_schema)
def get_food_service_ratings(json_data):
    if json_data.amount < 0 or json_data.offset < 0:
        raise ValueError("Amount and offset should not be negative!")
    user_id, _ = verify_token(json_data.token, json_data.user_type)
    servers_location = get_service_servers_location(user_id)
    ratings = get_ratings(
        user_id, json_data.stars, json_data.offset, json_data.amount)
    return {
        "servers_location": servers_location,
        "count": len(ratings),
        "ratings": ratings}


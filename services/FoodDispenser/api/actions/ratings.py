from api.api_hub import api_handler
from database.requests.rating_requests import get_services_list


json_schema = {
    "token": str,
    "amount": int
}


@api_handler.register_action("ratings.list", "consumer")
def get_services_ratings(json_data):
    pass

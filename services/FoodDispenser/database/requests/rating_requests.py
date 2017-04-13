from database.database_requests import db_request


def get_services_list(amount):
    with db_request("Ratings") as Ratings:
        pass

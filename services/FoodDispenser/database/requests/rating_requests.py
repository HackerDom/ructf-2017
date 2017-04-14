from database.database_requests import db_request
from database.requests.user_requests import username_to_user_id


def get_services_list(offset, amount):
    with db_request("User") as User:
        rows = User.select()\
            .order_by(User.id.desc())\
            .where(User.is_food_service)\
            .offset(offset)\
            .limit(amount)

    return [row.username for row in rows]


def rate_service(service_name, publisher_id, stars, comment):
    if not (isinstance(stars, int) and 1 <= stars <= 5):
        raise ValueError("Stars field should be int: from 1 to 5!")
    user_id = username_to_user_id(service_name)
    with db_request("Ratings") as Ratings:
        row = Ratings.select().where(
            (Ratings.food_service_id == user_id) &
            (Ratings.client_id == publisher_id)
        ).first()
    if row is not None:
        raise ValueError("You have already published your comment!")
    with db_request("Ratings") as Ratings:
        Ratings.insert(
            food_service_id=user_id,
            client_id=publisher_id,
            stars_amount=stars,
            comment_content=comment
        ).execute()


def get_ratings(service_id, stars, offset, amount):
    if not all([isinstance(element, int) for element in stars]):
        raise ValueError("Stars list should contain only ints")
    with db_request("Ratings") as Ratings:
        rows = Ratings.select().where(
            (Ratings.food_service_id == service_id) &
            Ratings.stars_amount << stars)\
            .offset(offset)\
            .limit(amount)
    return [{
        "stars": row.stars_amount,
        "comment": row.comment_content
            } for row in rows]

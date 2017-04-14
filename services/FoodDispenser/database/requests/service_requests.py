from database.database_requests import db_request


def get_services_list(offset, amount):
    with db_request("User") as User:
        rows = User.select()\
            .order_by(User.id.desc())\
            .where(User.is_food_service)\
            .offset(offset)\
            .limit(amount)
    return [row.username for row in rows]


def add_service_servers_location(user_id, private_info):
    if not(0 < len(private_info) < 256):
        raise ValueError("Bad private info")
    with db_request("User") as User:
        User.update(user_meta=private_info)\
            .where(User.id == user_id)\
            .execute()


def get_service_servers_location(user_id):
    with db_request("User") as User:
        row = User.select().where(User.id == user_id).first()
    return row.user_meta


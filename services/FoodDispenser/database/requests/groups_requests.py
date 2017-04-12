from database.database_requests import db_request
from peewee import IntegrityError


def create_user_group(creator_id, group_name):
    with db_request("Group") as Group:
        try:
            Group.insert(
                group_name=group_name,
                group_creator_id=creator_id
            ).execute()
        except IntegrityError:
            raise ValueError("This group already exists!")


def generate_invite_code(user_id, group):
    pass
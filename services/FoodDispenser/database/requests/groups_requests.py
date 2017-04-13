from database.database_requests import db_request
from peewee import IntegrityError
from json import loads, dumps
from database.requests.utils import generate_random_hash


def create_user_group(creator_id, group_name):
    with db_request("Group") as Group:
        try:
            Group.insert(
                group_name=group_name,
                group_creator_id=creator_id,
                group_invites_list="[]"
            ).execute()
        except IntegrityError:
            raise ValueError("This group already exists!")


def get_invites_list(group, user_id):
    with db_request("Group") as Group:
        row = Group.select().where(
            (Group.group_name == group) &
            (Group.group_creator_id == user_id)
        ).first()

    if row is None:
        raise ValueError("You don't own this group/this group doesn't exists")

    return loads(row.group_invites_list)


def generate_invite_code(user_id, group, amount):
    invite_codes_list = get_invites_list(group, user_id)
    invites = [generate_random_hash()[:32] for _ in range(amount)]
    invite_codes_list += invites

    with db_request("Group") as Group:
        Group.update(group_invites_list=dumps(invite_codes_list)).where(
            (Group.group_name == group) &
            (Group.group_creator_id == user_id)).execute()

    return invites


def add_user_to_group(user_id, group_name):
    with db_request("User") as User:
        row = User.select().where(User.id == user_id).first()
        user_groups_set = set(loads(row.user_groups))
        user_groups_set.add(group_name)
        User.update(
            user_groups=dumps(list(user_groups_set))).where(User.id == user_id)\
            .execute()


def activate_invite(user_id, group, invite_code):
    with db_request("Group") as Group:
        row = Group.select().where(Group.group_name == group).first()

    if row is None:
        raise ValueError("You don't own this group/this group doesn't exists")

    invite_codes_list = loads(row.group_invites_list)
    if invite_code in invite_codes_list:
        invite_codes_list.remove(invite_code)
        add_user_to_group(user_id, group)
        with db_request("Group") as Group:
            Group.update(group_invites_list=dumps(invite_codes_list)).where(
                Group.group_name == group).execute()
        return "Sucessfully added to {}".format(group)
    raise ValueError("Incorrect user group or invite code!")




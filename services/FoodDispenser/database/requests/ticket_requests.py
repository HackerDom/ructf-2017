from database.database_requests import db_request
from database.requests.user_requests import get_user_groups_list_by_user_id


def get_tickets_by_user_id(user_id):
    user_groups = get_user_groups_list_by_user_id(user_id)
    with db_request("TicketStorage") as TicketStorage:
        rows = TicketStorage.select().where(
            TicketStorage.ticket_target_group << user_groups
        ).execute()

    return [{
        "provider": row.ticket_provider,
        "code": row.ticket_code,
        "content": row.ticket_content
            } for row in rows]


def create_ticket(provider_name, code, content, target_group):
    with db_request("TicketStorage") as TicketStorage:
        TicketStorage.insert(
            ticket_provider=provider_name,
            ticket_code=code,
            ticket_content=content,
            ticket_target_group=target_group
        ).execute()

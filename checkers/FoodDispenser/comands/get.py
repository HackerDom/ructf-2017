import fd_api
import randomize
from comands import OK, MUMBLE, DOWN, CORRUPT, CHECKER_ERROR
from json import loads
from urllib.error import HTTPError
from base64 import b64decode


def get(host, flag_id, flag, vuln):
    if vuln == "1":
        return get_first_vuln(host, flag_id, flag)
    if vuln == "2":
        return get_second_vuln(host, flag_id, flag)


def get_first_vuln(host, flag_id, flag):
    join_info = loads(b64decode(flag_id).decode())
    target_group = join_info["group"]
    invites_list = join_info["invites"]

    try:
        username = randomize.generate_random_passenger_name()
        password = randomize.generate_random_hash()
        fd_api.Registration.register_user(host, username, password)
        user_token = fd_api.Tokens.get_user_token(host, username, password)
        for invite in invites_list:
            answer = fd_api.Groups.add_user_to_group(
                host, user_token, target_group, invite)
            if "result" in answer:
                tickets = fd_api.Tickets.get_user_tickets(
                    host, user_token
                )["result"]["ticket_objects"]
                for ticket in tickets:
                    if flag == ticket["code"]:
                        return {"code": OK}
                return {"code": CORRUPT}

        return {"code": CORRUPT}
    except HTTPError:
        return {"code": DOWN}
    except KeyError:
        return {"code": MUMBLE}


def get_second_vuln(host, flag_id, flag):
    token = flag_id
    return {"code": CHECKER_ERROR, "public": "Not implemented yet!"}
    # need to implement ssh connection to laptop!

import fd_api
import randomize
from comands import OK, MUMBLE, DOWN, CORRUPT, CHECKER_ERROR
from json import loads
from urllib.error import HTTPError
from base64 import b64decode
import paramiko
import traceback


SELENIUM_HOST_IP = "10.60.200.100"


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
    except HTTPError as e:
        return {"code": DOWN, "private": traceback.format_exc()}
    except KeyError as e:
        return {"code": MUMBLE, "private": traceback.format_exc()}


def get_second_vuln(host, flag_id, flag):
    token = flag_id
    received_flag = get_flag_by_selenium_over_ssh(host, token)
    if received_flag == flag:
        return {"code": OK}
    if received_flag == "Couldn't find flag":
        return {"code": MUMBLE}
    if received_flag == "Couldn't init driver":
        return {"code": CHECKER_ERROR}
    if received_flag == "Service response timed out":
        return {"code": DOWN}
    if received_flag == "Unhandled exception":
        return {"code": CHECKER_ERROR}
    return {"code": CHECKER_ERROR}


def get_flag_by_selenium_over_ssh(team_domain, token):
    """
    :param team_domain: <service>.teamN.ructf
    :param token: token (cookie)
    :return: extracted flag
    """
    ssh_username = team_domain.split(".")[1]  # extract teamN
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(
            SELENIUM_HOST_IP,
            username=ssh_username,
            key_filename="selenium",
            timeout=10
        )
        _, stdout, __ = ssh_client.exec_command(
            'python3 main.py {} {}'.format(team_domain, token))
        return [line.strip('\n') for line in stdout][0]
    except Exception as e:
        return "Couldn't init driver {}".format(traceback.format_exc())
    finally:
        try:
            ssh_client.close()
        except Exception:
            pass

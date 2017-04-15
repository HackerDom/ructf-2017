import fd_api
import randomize
from comands import OK, MUMBLE, DOWN, CORRUPT, CHECKER_ERROR
from json import loads
from urllib.error import HTTPError
from base64 import b64decode
import paramiko
import traceback


SELENIUM_HOST_IP = "10.60.201.100"
SELENIUM_HOST_KEY = b''


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
        return {"code": DOWN, "private": e}
    except KeyError as e:
        return {"code": MUMBLE, "private": e}


def get_second_vuln(host, flag_id, flag):
    token = flag_id
    #received_flag = get_flag_by_selenium_over_ssh(host, token)
    #if received_flag == flag:
    #    return {"code": OK}
    #if received_flag == "some_annoying_checker_error":
    #    return {"code": CHECKER_ERROR}

    return {"code": CHECKER_ERROR, "public": "Method not implemented yet!"}


def get_flag_by_selenium_over_ssh(team_domain, token):
    """
    :param team_domain: <service>.teamN.ructf
    :param token: token (cookie)
    :return: extracted flag
    """
    ssh_username = team_domain.split(".")[1]  # extract teamN
    key = paramiko.RSAKey(data=b64decode(SELENIUM_HOST_KEY))
    ssh_client = paramiko.SSHClient()
    ssh_client.get_host_keys().add(SELENIUM_HOST_IP, 'ssh-rsa', key)
    try:
        ssh_client.connect(
            SELENIUM_HOST_IP,
            username=ssh_username,
            timeout=15
        )
        _, stdout, __ = ssh_client.exec_command(
            'python3 selenium.py {} {}'.format(team_domain, token))
        return [line.strip('\n') for line in stdout][0]
    except Exception:
        return "some_annoying_checker_error"
    finally:
        try:
            ssh_client.close()
        except Exception:
            pass

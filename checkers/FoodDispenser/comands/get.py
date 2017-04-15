import fd_api
import randomize
from comands import OK, MUMBLE, DOWN, CORRUPT, CHECKER_ERROR
from json import loads
from urllib.error import HTTPError
from base64 import b64decode
import paramiko
import traceback


SELENIUM_HOST_IP = "10.60.201.100"
SELENIUM_HOST_KEY = b'''
MIIEpAIBAAKCAQEAw+lzODgER4CnXgDt2Qyyu7fM6wP+XDppHTaQFVfZj5LDnI4/
/+FfL+A9ZCZxhnMeod5ttgRcspf/KYaH3pNZXja90R2rvlhhAIHSYGYNoCq+CPtj
SYA9gq317qWKAApdE1aGqVWy7R26LmWlZbfI1EioueRr0HCJqUW5i/UMskySVy/4
E9ByXIRXqh7kv9R5v7DwJa6GRSSr1872ID8xpdUVOsP5zCVfgI/okEgrvKgjnG15
ThswosQKRwX+wNS2QcOB8P2XkK5AjkfPt8iOMmnIJ6RxaL1FwR4s6lGdVSaz/h1o
5AjnYK++choRBzqGHuGjiH6RFhZaKVHdH61bbwIDAQABAoIBAETlKP7BPEgE51a4
juxAee5n0aloKyA17lc2o+7NiRXjb+TzZXBPylCk1BIPLucwPrp/5ScYW5z2tOXe
iJNuUARAzfnnLElw/RPXk6sQ2IPV5CR2e1ESxw7YrF7zWhdvjZHKYOrV12lphdrh
JgwiWH7G2occ3AleOhsMCRc94uwkQQrAedVNQvs1qDTHpom4hcTa+SYuZ5HBUKs1
n3pUbzWI5kXMWBuJ04901LGRkPTgMaypyLD1wCcKpKxT2WfR2HCnm+XntMA7lBCn
GB4yB+LNtLMNfK70J8hSaWoYc17B4wkp6kya8lRb1REpzbhozDFqRw3dlV5GvHGL
8czY6VkCgYEA+GNGykQmqn1jrJazFZ0k7+6q3ImKOdBfpuH6D3ApAZ6ht3MEg20k
eJl+LEsD8rjguuaWCpsw90yg6Ib7Tgh6G6UJXyracL7R4mIiVLAEwE/wRLQbzKPv
cWrgWbJ1YI0TthRsCku1ighzyVDM0pG6g0aVhIjKeibA/nPSGWWqU5UCgYEAyep5
gaH0LV5tIRoQrX9EnB4ree7EHpoD35OxCafP+Dkjy6DGbZBgzhiMxi9ysQ/ws5P6
5T5VlxDcTQxm0iLJFCATVf9Ez9jMq1ivyRp3+IdziCy9+YyZxTmdXZqWXVYEYFlc
BgyqU+wCfhPRgU2P3cPSEGbU6+TbkKUzIODesfMCgYEArv1qEve+ceBSx3WIB1Ml
ga+YSjTP3/kwWibb/+JZ0V1Luy1Z4amTxy8EF/pldqvPD32B+UjqT196ATePdqM8
O5uipZxQNpwIy7+tRhKX1lC7CfwFlb9s4m+UTT0PuozJdT6f+wTpiax4vjyhgDvQ
tcmVbsDcPQBueRVp0CCyxZ0CgYEAsG1gnhSU9s97K2FLEU4S9RanhnNKijKpD8JM
/tLStWG4FUT2HOX6sBpjZwgufugeucqjf4tn3getduVPMm2SpTMhshLKXZJhw5ZK
gr3N9irkmCgAFvzzn5EoH5HjsMpoKIfsEJ0gdxPRWbiXZxQOkQd5lTtE8JmYAFtY
wXG7JGECgYBBt2Q2+pZ3ZkMxijoXXZuBMIDlFvzZs2WrGkSoH5VWY1LIzMd5Tkyu
RAx5k7+RbQA2nBammJBidV/ivo3jw4YmwVcidGbr9FWHVCtL76WdEzgVKcYJh9JK
oLWjkPRnb6EZZdSGcjFaCywTINrh5hbLZJJIpirT9b+UAL3qyRQxIA==
'''


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
    key = paramiko.RSAKey(data=b64decode(SELENIUM_HOST_KEY.replace(b'\n', b'')))
    ssh_client = paramiko.SSHClient()
    ssh_client.get_host_keys().add(SELENIUM_HOST_IP, 'ssh-rsa', key)
    try:
        ssh_client.connect(
            SELENIUM_HOST_IP,
            username=ssh_username,
            timeout=10
        )
        _, stdout, __ = ssh_client.exec_command(
            'python3 main.py {} {}'.format(team_domain, token))
        return [line.strip('\n') for line in stdout][0]
    except Exception:
        return "Couldn't init driver"
    finally:
        try:
            ssh_client.close()
        except Exception:
            pass

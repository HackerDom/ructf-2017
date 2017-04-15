import fd_api
import randomize
from comands import OK, MUMBLE, DOWN
from json import dumps
from urllib.error import HTTPError
from base64 import b64encode


def put(host, id, flag, vuln):
    if vuln == "1":
        return first_vuln_put(host, flag)
    if vuln == "2":
        return second_vuln_put(host, flag)


def check(host):
    first_check_result = first_vuln_put(host, randomize.rand_word(20))
    second_check_result = second_vuln_put(host, randomize.rand_word(20))
    third_check_result = special_check(host)
    return {"code":
            first_check_result["code"] and
            third_check_result["code"] and
            second_check_result["code"]}


def special_check(host):
    try:
        client_name = randomize.generate_random_passenger_name()
        client_password = randomize.generate_random_hash()
        service_name = randomize.generate_random_passenger_name()
        service_password = randomize.generate_random_hash()
        fd_api.Registration.register_service(host, service_name, service_password)
        fd_api.Registration.register_user(host, client_name, client_password)

        service_token = fd_api.Tokens.get_service_token(
            host, service_name, service_password)
        client_token = fd_api.Tokens.get_user_token(
            host, client_name, client_password)
        phrase = randomize.rand_word(20)
        fd_api.Ratings.rate_service(
            host,
            client_token,
            2,
            randomize.rand_word(20),
            service_name
        )
        ratings = fd_api.Ratings.get_food_service_ratings(
            host, service_token, [1, 2])["result"]["ratings"]
        for rating in ratings:
            if rating["comment"] == phrase:
                return {"code": OK}
        return {"code": MUMBLE}
    except HTTPError:
        return {"code": DOWN}
    except KeyError:
        return {"code": MUMBLE}


def first_vuln_put(host, flag):
    try:
        flag_poster = randomize.generate_random_service_name()
        flag_poster_password = randomize.generate_random_hash()
        fd_api.Registration.register_service(
            host, flag_poster, flag_poster_password)

        flag_poster_token = fd_api.Tokens.get_service_token(
            host, flag_poster, flag_poster_password)

        flag_poster_group = randomize.generate_random_hash()
        fd_api.Groups.create_group(host, flag_poster_token, flag_poster_group)

        invites = fd_api.Groups.group_get_invites(
            host, flag_poster_token, flag_poster_group)["result"]["invites"]
        fd_api.Tickets.add_tickets(
            host,
            flag_poster_token,
            flag,
            randomize.rand_word(15),  # todo clever word
            flag_poster_group
        )
    except HTTPError:
        return {"code": DOWN}
    except KeyError:
        return {"code": MUMBLE}
    return {"code": OK, "flag_id": b64encode(dumps(
        {"group": flag_poster_group, "invites": invites},
        separators=(',', ':')).encode()).decode()}


def second_vuln_put(host, flag):
    try:
        client_name = randomize.generate_random_passenger_name()
        client_password = randomize.generate_random_hash()
        service_name = randomize.generate_random_passenger_name()
        service_password = randomize.generate_random_hash()
        fd_api.Registration.register_service(
            host, service_name, service_password)
        fd_api.Registration.register_user(host, client_name, client_password)

        service_token = fd_api.Tokens.get_service_token(
            host, service_name, service_password)
        client_token = fd_api.Tokens.get_user_token(
            host, client_name, client_password)

        services_list = fd_api.Service.get_services_list(
            host, client_token)["result"]["services"]
        if service_name not in services_list:
            return {"code": MUMBLE}

        fd_api.Service.add_service_personal_info(host, service_token, flag)
        return {"code": OK, "flag_id": service_token}
    except HTTPError:
        return {"code": DOWN}
    except KeyError:
        return {"code": MUMBLE}

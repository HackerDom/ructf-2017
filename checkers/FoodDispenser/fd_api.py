from urllib.request import urlopen, Request
from json import loads, dumps

TIMEOUT = 5
API_PREFIX = "/api/v1"


def make_request(url, json):
    request_object = Request("http://" + url)
    request_object.data = dumps(json).encode()
    request_object.add_header("Content-Type", "text/plain")
    result = urlopen(request_object, timeout=5).read().decode()
    return loads(result)


class Groups:
    @staticmethod
    def add_user_to_group(host, token, group_name, group_invite):
        url = host + API_PREFIX + "/consumer/groups.join"
        data = {
            "token": token,
            "target_group": group_name,
            "group_invite": group_invite
        }
        answer = make_request(url, data)["response"]
        return answer

    @staticmethod
    def group_get_invites(host, token, group, invites_amount=3):
        url = host + API_PREFIX + "/food_service/groups.get_invites"
        data = {
            "token": token,
            "group": group,
            "invites_amount": invites_amount,
        }
        answer = make_request(url, data)["response"]
        return answer

    @staticmethod
    def create_group(host, token, group_name):
        url = host + API_PREFIX + "/food_service/groups.create"
        data = {
            "token": token,
            "group": group_name
        }
        answer = make_request(url, data)["response"]
        return answer


class Tickets:
    @staticmethod
    def add_tickets(host, token, ticket_code, ticket_content, ticket_target_group):
        url = host + API_PREFIX + "/food_service/tickets.add"
        data = {
            "token": token,
            "ticket_code": ticket_code,
            "ticket_content": ticket_content,
            "ticket_target_group": ticket_target_group
        }
        answer = make_request(url, data)["response"]
        return answer

    @staticmethod
    def get_user_tickets(host, token):
        url = host + API_PREFIX + "/consumer/tickets.get"
        data = {"token": token}
        tickets_list = \
            make_request(url, data)["response"]
        return tickets_list


class Registration:
    @staticmethod
    def register_user(host, username, password):
        url = host + API_PREFIX + "/consumer/register"
        data = {
            "username": username,
            "password": password
        }
        answer = make_request(url, data)["response"]
        return answer

    @staticmethod
    def register_service(host, username, password):
        url = host + API_PREFIX + "/food_service/register"
        data = {
            "username": username,
            "password": password
        }
        answer = make_request(url, data)["response"]
        return answer


class Tokens:
    @staticmethod
    def get_user_token(host, username, password):
        url = host + API_PREFIX + "/consumer/token"
        data = {
            "username": username,
            "password": password
        }
        token_field = make_request(url, data)["response"]["result"]["token"]
        return token_field

    @staticmethod
    def get_service_token(host, username, password):
        url = host + API_PREFIX + "/food_service/token"
        data = {
            "username": username,
            "password": password
        }
        token_field = make_request(url, data)["response"]["result"]["token"]
        return token_field


class Ratings:
    @staticmethod
    def rate_service(host, token, stars, comment, service_name):
        url = host + API_PREFIX + "/consumer/ratings.rate"
        data = {
            "token": token,
            "stars": stars,
            "comment": comment,
            "service_name": service_name
        }
        answer = make_request(url, data)["response"]
        return answer

    @staticmethod
    def get_food_service_ratings(host, token, stars: list, offset=0, amount=50):
        url = host + API_PREFIX + "/food_service/ratings.get"
        data = {
            "token": token,
            "offset": offset,
            "amount": amount,
            "stars": stars
        }
        answer = make_request(url, data)["response"]
        return answer


class Service:
    @staticmethod
    def get_services_list(host, token, amount=50, offset=0):
        url = host + API_PREFIX + "/consumer/services.list"
        data = {
            "token": token,
            "amount": amount,
            "offset": offset,
        }
        answer = make_request(url, data)["response"]
        return answer

    @staticmethod
    def add_service_personal_info(host, token, servers_location):
        url = "http://" + host + "/set_location?location={}"\
            .format(servers_location)
        request = Request(url)
        request.add_header("Cookie", "token={}".format(token))
        request.method = "GET"
        answer = urlopen(request, timeout=TIMEOUT).read().decode()
        return answer

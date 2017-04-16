#!/usr/bin/python3
# do stuff
import uuid
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from httpchecker import *
from randomizer import *

GET = 'GET'
POST = 'POST'


class StrongboxChecker(HttpCheckerBase, Randomizer):
    def session(self, addr):
        s = r.Session()
        s.headers[
            'User-Agent'
        ] = self.randUserAgent()
        s.headers['Accept'] = '*/*'
        s.headers['Accept-Language'] = 'en-US,en;q=0.5'
        return s

    def url(self, addr, suffix):
        return 'http://{}/{}'.format(addr, suffix)

    def parse_response(self, response):
        if response.status_code != 200:
            print(response.text)
            raise HttpWebException(response.status_code, response.url)
        try:
            result = {"url": response.url,
                      "page": BeautifulSoup(response.text, "html5lib")}

            return result
        except ValueError:
            raise response.exceptions.HTTPError('failed to parse response')

    def spost(self, s, addr, suffix_post, data=None):
        response = s.post(self.url(addr, suffix_post), data, timeout=10)
        return self.parse_response(response)

    def sget(self, s, addr, suffix):
        response = s.get(self.url(addr, suffix), timeout=10)
        return self.parse_response(response)

    def randword(self):
        word = ''
        rnd = random.randrange(2, 10)
        for i in range(rnd):
            word += random.choice(string.ascii_lowercase)
        return word

    def checkSignup(self, result):
        try:
            if result["page"].title.text.strip() == 'Sign in':
                return False
            return True
        except (AttributeError, TypeError):
            return True

    def checkSignin(self, result):
        try:
            exit_element = result["page"].find_all("a")
            if len(exit_element):
                for element in exit_element:
                    if element.text.strip() == 'Sign out':
                        return False
                return True
            return True
        except (AttributeError, TypeError):
            return True

    def checkAddOrder(self, result, order):
        try:

            title = result["page"].title
            if title and title.text.strip().startswith('Order {} #'.format(
                    order['name']
            )) > -1:
                return False
            return True
        except (AttributeError, TypeError):
            return True

    def checkAddOrderItem(self, result, flag):
        try:
            if result["page"].text.find(flag) > -1:
                return False
            return True
        except (AttributeError, TypeError):
            return True

    def getOrderId(self, result):
        title = result["page"].title.text.strip()
        pos_id = title.find('#')
        return title[pos_id + 1:]

    def getOrderItem(self, coordinates):
        order_items = []
        while len(coordinates):
            order_item = {
                'position_x': coordinates[:2][0],
                'position_y': coordinates[:2][1],
                'quantity_energy': random.randrange(1, 100)
            }
            coordinates = coordinates[2:]
            order_items.append(order_item)
        return order_items

    def put(self, addr, flag_id, flag, vuln):
        session = self.session(addr)
        user = self.randUser()
        order = {
            'name': self.randword()
        }
        flag_order_item = uuid.uuid4().hex
        if vuln == 1:
            user['private_type'] = 'on'
            user['giro'] = flag
            order_items = self.getOrderItem(flag_order_item[:16])
            order['secret_code'] = flag_order_item[16:]
        else:
            user['giro'] = uuid.uuid4().hex
            order_items = self.getOrderItem(flag[:16])
            order['secret_code'] = flag[16:]
            flag_order_item = flag
        result = self.spost(session, addr, 'signup/', user)
        check_signup = self.checkSignup(result)
        if check_signup:
            print('registration failed')
            return EXITCODE_MUMBLE
        result = self.spost(session, addr, 'signin/', {
            'login': user['login'],
            'password': user['password']
        })
        check_signin = self.checkSignin(result)
        if check_signin:
            print('login failed')
            return EXITCODE_MUMBLE

        result = self.spost(session, addr, 'order/add/', order)
        check_add_order = self.checkAddOrder(result, order)
        if check_add_order:
            print('add order failed')
            return EXITCODE_MUMBLE
        order['id'] = self.getOrderId(result)
        check_add_order = self.checkAddOrder(result, order)
        for order_item in order_items:
            result = self.spost(
                session, addr,
                'order/{}/add_item/'.format(order['id']),
                order_item
            )
        result = self.sget(session, addr, 'order/{}/'.format(order['id']))
        check_add_order_item = self.checkAddOrderItem(
            result,
            flag_order_item
        )
        if check_add_order_item:
            print('add order item failed')
            return EXITCODE_MUMBLE
        print(
            '{}:{}:{}'.format(
                user['login'],
                user['password'],
                order['id']
            )
        )
        return EXITCODE_OK

    def get(self, addr, flag_id, flag, vuln):
        session = self.session(addr)
        parts = flag_id.split(':', 3)
        user = {
            'login': parts[0],
            'password': parts[1]
        }

        result = self.spost(
            session, addr, 'signin/', {
                'login': parts[0],
                'password': parts[1]
            }
        )

        check_signin = self.checkSignin(result)
        if check_signin:
            print('login failed')
            return EXITCODE_MUMBLE
        if vuln == 1:
            pass
            # result = self.sget(session, addr, 'user/')
            # if result["page"].text.find(flag[16:]) <= -1:
            #     print('flag not found user')
            #     return EXITCODE_CORRUPT
        else:
            result = self.sget(session, addr, 'order/{}/'.format(parts[2]))
            check_add_order_item = self.checkAddOrderItem(
                result,
                flag
            )
            if check_add_order_item:
                print('flag not found in order')
                return EXITCODE_CORRUPT
        return EXITCODE_OK

    def check(self, addr):
        session = self.session(addr)
        user = self.randUser()
        order = {
            'name': self.randword()
        }

        flag_order_item = uuid.uuid4().hex
        user['private_type'] = 'on'
        user['giro'] = uuid.uuid4().hex
        order_items = self.getOrderItem(flag_order_item[:16])
        order['secret_code'] = flag_order_item[16:]
        result = self.spost(session, addr, 'signup/', user)

        check_signup = self.checkSignup(result)
        if check_signup:
            print('registration failed')
            return EXITCODE_MUMBLE
        result = self.spost(session, addr, 'signin/', {
            'login': user['login'],
            'password': user['password']
        })
        check_signin = self.checkSignin(result)

        if check_signin:
            print('login failed')
            return EXITCODE_MUMBLE
        result = self.spost(session, addr, 'order/add/', order)
        check_add_order = self.checkAddOrder(result, order)
        if check_add_order:
            print('add order failed')
            return EXITCODE_MUMBLE
        order['id'] = self.getOrderId(result)
        check_add_order = self.checkAddOrder(result, order)
        for order_item in order_items:
            result = self.spost(
                session, addr,
                'order/{}/add_item/'.format(order['id']),
                order_item
            )
        result = self.sget(session, addr, 'order/{}/'.format(order['id']))
        check_add_order_item = self.checkAddOrderItem(
            result,
            flag_order_item
        )
        if check_add_order_item:
            print('add order item failed')
            return EXITCODE_MUMBLE
        return EXITCODE_OK


StrongboxChecker().run()

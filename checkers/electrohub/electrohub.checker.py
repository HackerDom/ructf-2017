#!/usr/bin/python3
# do stuff
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from .httpchecker import *
from .randomizer import *

GET = 'GET'
POST = 'POST'
PORT = 3000


class StrongboxChecker(HttpCheckerBase, Randomizer):
    def session(self, addr):
        s = r.Session()
        s.headers[
            'User-Agent'
        ] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
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

    def spost(self, s, addr, suffix_get, suffix_post, data=None):
        response = s.post(self.url(addr, suffix_post), data, timeout=5)
        return self.parse_response(response)

    def sget(self, s, addr, suffix):
        response = s.get(self.url(addr, suffix), timeout=5)
        return self.parse_response(response)

    def randword(self):
        word = ''
        rnd = random.randrange(2, 10)
        for i in range(rnd):
            word += random.choice(string.ascii_lowercase)
        return word

    def put(self, addr, flag_id, flag, vuln):
        session = self.session(addr)
        return EXITCODE_OK

    def get(self, addr, flag_id, flag, vuln):
        session = self.session(addr)
        return EXITCODE_OK

    def check(self, addr):
        session = self.session(addr)
        return EXITCODE_OK


StrongboxChecker().run()

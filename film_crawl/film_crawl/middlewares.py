import os
import fake_useragent


class RandomUserAgentMiddleware(object):
    def get_header(self):
        location = os.getcwd() + '/fake_useragent.json'
        ua = fake_useragent.UserAgent(path=location)
        return ua.random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.get_header()

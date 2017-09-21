#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Response():
    def __init__(self, message):
        self.body = message[8:]

    @staticmethod
    def fxl(message):
        body = message[8:].decode('utf-8')
        kvArr = list(map(lambda x: x.split('@='),
                         list(filter(lambda x: x.strip() is not '', body.split('/')))))
        d = {}
        for kv in kvArr:
            key = kv[0].replace('@S', '/').replace('@A', '@')
            value = kv[0].replace('@S', '/').replace('@A', '@')
            d[key] = value
        return d

    def xl(self):
        pass

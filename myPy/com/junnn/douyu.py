#! /usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
import re
import socket
from pymongo import MongoClient
import sys

import os

import time

# 连接mongodb数据库
mc = MongoClient('mongodb://mini1:27017/')

db = mc.douyuMsg
txt_coll = db.message


class Tcp_connect(object):
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def re_conn(self, host, port):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))


host = 'openbarrage.douyutv.com'

port = 8601

type_ = re.compile('type@=.*/?')

file = open('d://testB.txt', 'ab')

health_flag = 0


def fxl(msg):
    # print(b'----' + body)
    try:
        # body = type_.search()
        body = msg.decode('utf-8')
    except UnicodeDecodeError as e:
        print('error--%s' % msg)
        return {}

    kvArr = list(map(lambda x: x.split('@='),
                     list(filter(lambda x: x is not '', body.split('/')))))
    kvArr.pop(-1)
    d = {}
    for kv in kvArr:
        if kv.__len__() == 2:
            key = kv[0].replace('@S', '/').replace('@A', '@')
            value = kv[1].replace('@S', '/').replace('@A', '@')
            d[key] = value
        else:
            print('error kv' + kv)
    return d


def sendmsg(msgstr, client):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def keeplive(client):
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\x00'
        print('init live')
        sendmsg(msg, client)
        time.sleep(15)


def go(roomId, client):
    login = 'type@=loginreq/roomid@=%s/\x00' % (roomId,)
    sendmsg(login, client)
    print(client.recv(1024))
    joingroup = 'type@=joingroup/rid@=%s/gid@=-9999/\x00' % (roomId,)
    sendmsg(joingroup, client)
    while True:
        try:
            head = client.recv(12)
            if len(head) < 12:
                head = head + client.recv(12 - len(head))
            # print(head)
            data_length = int.from_bytes(head[:4], 'little') - 8
            data = client.recv(data_length)
            while len(data) < data_length:
                data = data + client.recv(data_length - len(data))
            message = fxl(data)
            txt_coll.insert({'roomId': roomId, 'msg': message})
            code = message.get('code')
            if None is not code:
                return 1
            if 'chatmsg' == message.get('type'):
                print('%s : %s' % (message.get('nn'), message.get('txt')))
                # print(message)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return 1

    return 1


if __name__ == '__main__':
    while True:
        c = Tcp_connect(host, port)

        p1 = multiprocessing.Process(target=go, args=(58428, c.client))
        p2 = multiprocessing.Process(target=keeplive, args=(c.client,))
        p1.start()
        p2.start()

        while p1.exitcode is None:
            time.sleep(3)

        p1.terminate()
        p2.terminate()
        print('re start')
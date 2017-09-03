#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import pyperclip
import time
import sys


local_ip = sys.argv[1]
remote_ip = sys.argv[2]
port = sys.argv[3]
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class clip(object):
    def __init__(self):
        self.clipData = self.readClip()

    def readClip(self):
        return pyperclip.paste()

    def writeClip(self, data):
        print('copy %s' % data)
        self.clipData = data
        pyperclip.copy(data)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def sentData(data):
    # 发送数据:
    print('send ' + data)
    client.sendto(data.encode('utf-8'), (remote_ip, 8888))
    # 接收数据:
    # print(s.recv(1024).decode('utf-8'))
    # client.close()


def checkClip(clip):
    if clip.clipData != clip.readClip():
        clip.clipData = clip.readClip()
        return clip.clipData
    else:
        return None


c = clip()


def loop_check_clip():
    while True:
        d = checkClip(c)
        if d is not None:
            sentData(d)
        time.sleep(1)


def clip_server():
    # 绑定端口:
    server.bind((local_ip, 8888))
    print('Bind UDP on 8888...')
    while True:
        # 接收数据:
        data, addr = server.recvfrom(1048576)
        clipdata = data.decode('utf-8')
        c.writeClip(clipdata)
        server.sendto(b'ok', addr)


if __name__ == '__main__':
    t = threading.Thread(target=loop_check_clip, name='check_clip')
    t.start()
    t1 = threading.Thread(target=clip_server, name='clip_server')
    t1.start()

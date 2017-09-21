#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

from com.junnn.clip import *


def sentData(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 发送数据:
    print(data)
    s.sendto(data.encode('utf-8'), ('192.168.33.8', 8888))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
    s.close()


def checkClip(clip):
    if clip.clipData != clip.readClip():
        clip.clipData = clip.readClip()
        return clip.clipData
    else:
        return None


if __name__ == "__main__":
    c = clip()
    while True:
        d = checkClip(c)
        if d is not None:
            sentData(d)
        time.sleep(1.5)

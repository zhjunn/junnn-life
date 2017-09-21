#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pyperclip


class clip(object):

    def __init__(self):
        self.clipData = self.readClip()

    def readClip(self):
        return pyperclip.paste()

    def writeClip(self, data):
        print('copy %s' % data)
        pyperclip.copy(data)

#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        assert isinstance(value, int)
        self._score = value




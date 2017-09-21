#! /usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector

conn = mysql.connector.connect(host='mini1', user='root', password='Root1234', database='zhangsan')

cur = conn.cursor()
cur.execute('show tables;')
value = cur.fetchall()
print(value)

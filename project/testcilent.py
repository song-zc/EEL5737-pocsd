# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 16:05:11 2020

@author: Jonathan
"""

import xmlrpc.client
import socket

from time import sleep

proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")
try:
    print(proxy.add(2, 5))

except xmlrpc.client.Fault as err:
    print("A fault occurred")
    print("Fault code: %d" % err.faultCode)
    print("Fault string: %s" % err.faultString)

sleep(5)

print ('sleep end')

try:
    print(proxy.add(2, 5))
except socket.error as err:
    print("A fault occurred")
    print(err)
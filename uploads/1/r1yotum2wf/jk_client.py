#!/usr/bin/env python
# coding:utf8
from socket import *
from time import sleep
import os

HOST = 'monitoring_service'
PORT = 21567
BUFSIZ = 2048
ADDR = (HOST, PORT)

while True:
    try:
        udpCliSock = socket(AF_INET, SOCK_DGRAM)
        udpCliSock.connect(ADDR)            #尝试连接
        data = os.popen("free  | head -2 | tail -1 | awk '{print $2,$3}'").read().strip('\n') +\
                ' ' + os.popen("vmstat 1 2|  tail -1 | awk -F ' ' '{print $15}'").read().strip('\n') +\
                ' ' + os.popen("df | grep sda1 | awk '{print $6,$2,$3}'").read().strip('\n')+\
                ' ' + os.popen("df | grep sdb2 | awk '{print $6,$2,$3}'").read().strip('\n') + \
                ' ' + os.popen("expr `docker ps | wc -l` - 1").read().strip('\n')+\
	        ' ' + os.popen("expr `docker ps -a | wc -l` - 1").read().strip('\n')+\
                ' ' + os.popen("sar -n DEV 1 1 | grep em1 | head -1 | awk '{print $6,$7}'").read().strip('\n')
        udpCliSock.send(data)               #发送消息
        udpCliSock.close()                  #关闭客户端连接
    except:
        print 'error :connect fail'
    sleep(3)

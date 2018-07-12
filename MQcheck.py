# !/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket
import time
import pika
import os
import sys

username = 'admin'        # mq用户
password = 'admin'        # 用户密码
mqip = '127.0.0.1'        # mq地址
mqlist = sys.argv[1]      # 消息队列名称,外部传入参数
mqport = 5672

starttime = time.time()   # 定义开始时间

def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    t =  time.time() - starttime
    curl(t)
    exit()
# 客户端消费为持续经常，exit每消费一次退出持续
def curl(time):
    #os.system("curl -h %s" % (time))
    #curl 命令，%s为变量
    print time

def check_aliveness(ip, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(mqip ,mqport ,'/' ,credentials))
        channel = connection.channel()
        channel.queue_declare(queue=mqlist)
        channel.basic_publish(exchange='',
                              routing_key=mqlist ,
                              body='test')

        channel.basic_consume(callback, queue=mqlist)
        channel.start_consuming()

    except Exception:
        curl(500)
    finally:
        sk.close()

check_aliveness(mqip , mqport)


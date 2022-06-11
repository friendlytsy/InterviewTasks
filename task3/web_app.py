# Задача 3
# Написать клиент-серверную систему, работающую по следующему алгоритму:
# 	•	Сервер держит открытыми порты 8000 и 8001.
# 	•	При запуске клиент выбирает для себя уникальный идентификатор.
# 	•	Клиент подключается к серверу к порту 8000, передает ему свой идентификатор и получает от сервера уникальный код.
# 	•	Клиент подключается к серверу к порту 8001 и передает произвольное текстовое сообщение, свой идентификатор и код, полученный на шаге 2.
# 	•	Если переданный клиентом код не соответствует его уникальному идентификатору, сервер возвращает клиенту сообщение об ошибке.
# 	•	Если код передан правильно, сервер записывает полученное сообщение в лог.
# Сервер должен поддерживать возможность одновременной работы с хотя бы 50 клиентами.
# Для реализации взаимодействия между сервером и клиентом системы допускается (но не требуется) использование высокоуровнего протокола (например, HTTP).

import json
from flask import Flask, request, jsonify
import random

import redis

import logging

# Config logging
from logging.config import fileConfig

fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Redis config
redis_host = 'localhost'
redis_port = 6379
redis_password = ''

app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def create_endpoint():
    # Loads data from json
    record = json.loads(request.data)
    # Open connection to redis
    r = open_redis()
    
    reply_data = {}
    # If endpoint id exist, notify client about that
    if r.exists(record['id']):
        reply_data['message'] = 'Endpoint already exist'
        reply_data['code'] = r.get(record['id'])
    else:
        # Preparing code for the client
        reply_data['message'] = 'Endpoint created'
        reply_data['code'] = random.randint(1000,9999)
        r.set(record['id'], reply_data['code'])
    
    return jsonify(reply_data)

@app.route('/echo', methods=['POST'])
def echo_message():
    # Loads data from json
    record = json.loads(request.data)
    # Open connection to redis
    r = open_redis()
    reply_data = {}
    # If key exit
    if r.exists(record['id']):
        # If key:value equal to code from json
        print(r.get(record['id']))
        print(record['code'])
        if int(r.get(record['id'])) == record['code']:
            # Putting message from json to reply
            reply_data['message'] = 'messages recored at log file'
            log_msg = 'Endpoint id and code is correct, the message is: ' + record['message']
            logger.info(log_msg)
            # Reply to client
            return jsonify(reply_data)
        else:
            # key:value is not equal to code from json
            reply_data['reason'] = 'code is incorrect'
            # Reply to client
            return jsonify(reply_data), 401
    else:
        # Key not exist
        reply_data['reason'] = 'endpoint is not exist'
        # Reply to client
        return jsonify(reply_data), 401  

def open_redis():
    # create the Redis Connection object
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8. 
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    return r
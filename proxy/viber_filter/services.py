import hashlib
import redis
import json

r = redis.Redis()
start_reply = {
    "min_api_version": 8,
    "type": "text",
    "text": "Добро пожаловать! Это сообщение по-умолчанию, обратитесь к менеджерам, чтоб его изменить.",
    "sender": {
        "name": "Автоматический ответ",
        "avatar": None
    }
}


def hash_message(msg):
    m = hashlib.sha256()
    m.update(msg)
    return m.hexdigest()


def add_to_queue(data):
    event = data.get('event', None)
    if event == 'message':
        encoded_data = json.dumps(data).encode('utf-8')
        hash_key = hash_message(encoded_data)
        if not r.exists(hash_key):
            r.set(hash_key, encoded_data)
        result = None
    elif event == 'conversation_started':
        result = start_reply
    else:
        result = {}
    return result
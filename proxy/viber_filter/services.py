import hashlib
import redis
import json

from viber_filter.replies import REPLIES

r = redis.Redis()
# start_reply = {
#     "min_api_version": 8,
#     "type": "text",
#     "text": "Добро пожаловать! Это сообщение по-умолчанию, обратитесь к менеджерам, чтоб его изменить.",
#     "sender": {
#         "name": "Автоматический ответ",
#         "avatar": None
#     }
# }


def hash_message(msg):
    m = hashlib.sha256()
    m.update(msg)
    return m.hexdigest()


def add_to_queue(data):
    try:
        event = data.get('event', None)
        if event == 'message':
            encoded_data = json.dumps(data).encode('utf-8')
            hash_key = hash_message(encoded_data)
            if not r.exists(hash_key):
                r.sadd('hashkeys', hash_key)
                r.set(hash_key, encoded_data)
                for key in list(r.smembers('hashkeys'))[:2]:
                    message = r.get(key)
                    r.delete(key)
                    r.srem('hashkeys', key)
                    print(message)
                    print(r.smembers('hashkeys'))
        return REPLIES[event]
    except Exception:
        return {}

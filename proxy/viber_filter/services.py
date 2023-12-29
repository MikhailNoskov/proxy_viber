import hashlib
import redis
import json

from viber_filter.replies import REPLIES

r = redis.Redis()


def hash_message(message):
    """
    Хэширование сообщений
    :param message:
    :return:
    """
    m = hashlib.sha256()
    m.update(message)
    return m.hexdigest()


def add_to_queue(data):
    """
    Добавка сообщений с ивенотом месседж в 'очередь на отправку' в рэдисе
    :param data:
    :return:
    """
    # try:
    event = data.get('event', None)
    if event == 'message':
        encoded_data = json.dumps(data).encode('utf-8')
        hash_key = hash_message(encoded_data)
        if not r.exists(hash_key):
            r.sadd('hashkeys', hash_key)
            r.set(hash_key, encoded_data)
    return REPLIES[event]
    # except Exception:
    #     return {}

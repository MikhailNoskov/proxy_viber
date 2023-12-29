import hashlib
import redis
import json
from logging import getLogger


from viber_filter.replies import REPLIES

logger = getLogger('queue_logs')
logger_2 = getLogger('main_logs')

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
    try:
        event = data.get('event', None)
        if event == 'message':
            encoded_data = json.dumps(data).encode('utf-8')
            hash_key = hash_message(encoded_data)
            if not r.exists(hash_key):
                r.sadd('hashkeys', hash_key)
                r.set(hash_key, encoded_data)
                logger.debug(msg=f'New message {hash_key} added to queue')
        return REPLIES[event]
    except Exception as err:
        logger.warning(msg=f'Warning! Exception! {err}')
        return {}


def log_main(header, data):
    logger_2.debug(msg=header)
    logger_2.info(msg=data)
    return
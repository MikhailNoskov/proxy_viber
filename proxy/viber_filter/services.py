import hashlib
import redis
import json
from logging import getLogger
from datetime import datetime, timedelta

from viber_filter.replies import REPLIES
from viber_filter.tasks import send_single_to_main


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
    headers = {
        'Content-Type': 'application/json',
    }
    try:
        event = data.get('event', None)
        if event == 'message':
            encoded_data = json.dumps(data).encode('utf-8')
            hash_key = hash_message(encoded_data)
            hashkeys = r.smembers('hashkeys')
            if hash_key not in hashkeys:
                r.sadd('hashkeys', hash_key)
                kwargs = {
                    'hash_key': hash_key,
                    'message_data': encoded_data
                }
                task = send_single_to_main.apply_async(
                    kwargs=kwargs, eta=datetime.now() + timedelta(seconds=len(hashkeys) % 8)
                )
                headers['X-Celery-ID'] = task.id
                logger.debug(msg=f'New message {hash_key} added to queue')
        return REPLIES[event], headers
    except Exception as err:
        logger.warning(msg=f'Warning! Exception! {err}')
        return {}, headers


def log_main(header, data):
    logger_2.debug(msg=header)
    logger_2.info(msg=data)
    return

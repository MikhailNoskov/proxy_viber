import threading

from celery import shared_task
import redis
import json
import requests
from logging import getLogger

logger = getLogger('celery_logs')
r = redis.Redis()


@shared_task(bind=True, max_retries=5)
def resend_to_main(self):
    """
    Периодическая по отправке запросов на главный сервис
    :param self:
    :return:
    """
    try:
        task_id = resend_to_main.request.id
        keys = list(r.smembers('hashkeys'))[:8]
        logger.info(msg=keys)
        threads = []
        for key in keys:
            message = r.get(key)
            headers = {
                'Content-Type': 'application/json',
                'X-Celery-ID': task_id
            }
            # Абстрактеый урл главного сервиса
            # url = 'https://chatbot.com/webhook'
            url = 'http://127.0.0.1:8000/viber_messages/main/'

            thread = threading.Thread(target=send_request_to_main, args=(url, key, headers, message))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    except Exception as error:
        logger.error(msg=error)
        self.retry(error)


@shared_task(bind=True, max_retries=5)
def flush_celery_tasks(self):
    """
    Очистка рэдиса от задач селери
    :param self:
    :return:
    """
    try:
        keys = r.keys(f'celery-task-meta-*')
        r.delete(*keys)
        logger.debug(msg='Celery tasks have been flushed')
    except Exception as error:
        self.retry(error)


def send_request_to_main(url, key, headers, message):
    try:
        response = requests.post(url=url, headers=headers, json=json.loads(message))
        logger.info(msg=f'Message with {key} hash has been sent')
        logger.info(msg=response.status_code)

        r.delete(key)
        r.srem('hashkeys', key)
    except Exception as err:
        pass

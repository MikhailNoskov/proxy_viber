import threading

from celery import shared_task
import redis
import json
import requests
from logging import getLogger

logger = getLogger('celery_logs')
r = redis.Redis()


@shared_task(bind=True, max_retries=1)
def send_single_to_main(self, **kwargs):
    """
    Периодическая по отправке запросов на главный сервис
    :param self:
    :return:
    """
    task_id = send_single_to_main.request.id
    try:
        # Абстрактеый урл главного сервиса
        # url = 'https://chatbot.com/webhook'
        url = 'http://127.0.0.1:8000/viber_messages/main/'
        headers = {
            'Content-Type': 'application/json',
            'X-Celery-ID': task_id
        }
        key = kwargs['hash_key']
        message = kwargs['message_data']
        response = requests.post(url=url, headers=headers, json=json.loads(message))
        logger.info(msg=f'Message with {key} hash has been sent')
        logger.info(msg=response.status_code)
        r.srem('hashkeys', key)
    except Exception as error:
        logger.error(msg=error)
        self.retry(error)

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
        # Здесь вместо цикла можно пульнуть через threading. Оставил пока так
        for key in list(r.smembers('hashkeys'))[:8]:
            message = r.get(key)
            headers = {
                'Content-Type': 'application/json',
                'X-Celery-ID': task_id
            }
            # Абстрактеый урл главного сервиса
            # url = ''
            # requests.post(url=url, headers=headers, json=json.loads(message))
            logger.info(msg=f'Message with {key} hash has been sent')
            r.delete(key)
            r.srem('hashkeys', key)
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
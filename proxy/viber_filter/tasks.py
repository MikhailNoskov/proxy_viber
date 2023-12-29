from celery import shared_task
import redis

r = redis.Redis()


@shared_task(bind=True, max_retries=5)
def resend_to_main(self):
    try:
        task_id = resend_to_main.request.id
        for key in list(r.smembers('hashkeys'))[:2]:
            message = r.get(key)
            r.delete(key)
            r.srem('hashkeys', key)
    except Exception as error:
        self.retry(error)


@shared_task(bind=True, max_retries=5)
def flush_celery_tasks(self):
    try:
        keys = r.keys(f'celery-task-meta-*')
        r.delete(*keys)
    except Exception as error:
        self.retry(error)
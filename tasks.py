from celery import Celery
from requests import post
from time import sleep

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task(bind=True, max_retries=5)
def execute_webhook(self, webhook_url, headers):
    try:
        response = post(webhook_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to execute webhook: {e}")
        sleep(2 ** self.request.retries)  # Exponential backoff
        self.retry(exc=e)

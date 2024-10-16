import time
from celery import Celery

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    sleep_time = 60 * 1

    time.sleep(sleep_time)

    return x + y

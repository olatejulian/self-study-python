'''
Description:
------------

Examples:
---------
# queued_jobs_id = queue.job_ids # Gets a list of job IDs from the queue
# queued_jobs = queue.jobs # Gets a list of enqueued job instances
# job = queue.fetch_job('job_id') # Returns job having ID "my_id"
# queue.empty()
# queue.delete(delete_jobs=True)
'''
import time
import redis
from celery import Celery

from app_service import AppService

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


redis_connection = redis.Redis()


service = AppService(redis_connection)

number_of_iterations = 1e7

service.calculate_pi(1e7)

from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery()


@app.task()
def print_task():
    print("I just ran a task")
    # Do something...

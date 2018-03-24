from __future__ import absolute_import, unicode_literals
from celery import Celery
from . import search
import datetime

app = Celery()


@app.task()
def bulk_index_task():
    print("STARTED INDEXING AT " + str(datetime.datetime.now()))
    search.bulk_index_acordaos(True, 45)
    print("FINISHED INDEXING AT " + str(datetime.datetime.now()))

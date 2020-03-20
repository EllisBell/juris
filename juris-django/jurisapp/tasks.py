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


@app.task()
def recreate_index_from_db():
    print("STARTED RECREATING INDEX AT " + str(datetime.datetime.now()))
    search.delete_acordao_idx()
    search.create_acordao_idx()
    search.bulk_index_acordaos_alt(False, 45)
    print("FINISHED RECREATING INDEX AT " + str(datetime.datetime.now()))

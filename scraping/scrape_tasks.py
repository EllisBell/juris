from celery import Celery
from celery.schedules import crontab
import scrape_controller as sc

app = Celery('scrape_tasks', broker='redis://localhost:6379')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Scrapes everything at 23:00
    sender.add_periodic_task(crontab(minute=0, hour=23), run_scrape.s(), name='nightly scrape')


@app.task
def run_scrape():
    # time limit is in seconds
    sc.scrape_tribs(time_limit=18000)




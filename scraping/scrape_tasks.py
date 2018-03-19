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
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(30.0, test_scrape_task.s(), name='print every 30')


@app.task
def run_scrape():
    # time limit is in seconds
    sc.scrape_tribs(time_limit=18000)


@app.task
def test_scrape_task():
    # time limit is in seconds
    print("I am a scrape task!")

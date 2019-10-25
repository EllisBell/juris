from celery import Celery
from celery.schedules import crontab
import scrape_controller as sc
import smtplib
from email.mime.text import MIMEText
import os

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
    sender.add_periodic_task(crontab(hour=5, minute=0, day_of_week=6), run_dep_dups_del.s(), name='dups deletion')


@app.task
def run_scrape():
    # time limit is in seconds
    try:
        all_errors = sc.scrape_tribs(time_limit=14400)
        new = sc.get_newly_saved()
        send_scrape_report_email(new, all_errors)
    except Exception as e:
        send_scrape_error_email(str(e))

@app.task
def run_dep_dups_del():
    sc.delete_deprecated_dups(10800)


# TODO consider doing this in django instead?
# todo or with sentry
def send_scrape_report_email(new_counts, all_errors):
    subject = "The Daily Scrape"
    report = "The Daily Scrape\n\n"
    if new_counts:
        for trib_count in new_counts:
            report += trib_count[0] + ": " + str(trib_count[1]) + "\n"
        report += "\n\n"
        for error in all_errors:
            report += error + "\n"
    else:
        report += "Nothing new to report"

    send_email(subject, report)


# consider adding sentry to here, to log error and maybe to send email as well (even if goes well)
def send_scrape_error_email(error_message):
    send_email("Scrape Issues", error_message)


def send_email(subject, body):
    # Define to/from
    sender = os.environ.get('JURIS_EMAIL')
    recipient = os.environ.get('ADMIN_EMAIL')

    # Create message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.zoho.eu', 465)

    # Perform operations via server
    # n.b. actually logging in as recipient as that's my username for this account lol
    server.login(recipient, os.environ.get('JURIS_EMAIL_PW'))
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()

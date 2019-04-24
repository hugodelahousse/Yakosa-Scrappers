import os
from celery import Celery
from celery.schedules import crontab

app = Celery('scrappers', broker=os.getenv('CELERY_BROKER'))

app.conf.beat_schedule = {
    'run_scrapper': {
        'task': 'tasks.run_scrappers',
        'schedule': 10,
        'args': ('test',),
    }
}

@app.task
def sample_scrapper():
    print('Called sample scrapepr')

SCRAPPERS = {
    'test': sample_scrapper,
}

@app.task
def run_scrappers(*scrappers):
    for scrapper in scrappers:
        SCRAPPERS[scrapper].apply_async()

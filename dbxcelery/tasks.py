# Basic imports
import sys
import os
import configparser
import django
from celery import Celery

sys.path.insert(0, os.path.abspath("./filetracker"))
sys.path.insert(0, os.path.abspath("."))
# Dropbox
from dbxconn.dbxconn import DBXRepo

# Django models
os.environ['DJANGO_SETTINGS_MODULE'] = 'filetracker.settings'
django.setup()
from tracker.models import FileHistory, FileEntity

# TODO: Move this somewhere else
config = configparser.ConfigParser()
config.read(os.path.abspath('./config.ini'))

# Celery application
BROKER_URL = 'amqp://{}:{}@localhost:5672/{}'.format(config['Celery']['User'],
                                                     config['Celery']['Password'],
                                                     config['Celery']['VHost'])
app = Celery('tasks', broker=BROKER_URL)

# Dropbox repository object
TOKEN = config['Dropbox']['API_TOKEN']
repo = DBXRepo(TOKEN)


@app.task
def initialize_new_file(f):
    pass


@app.task
def update_file_metadata(f):
    """
    Given a filename update its modification history based on whether
    or not the file has been updated in Dropbox.
    """
    data = repo.get_file_metadata(f)
    if data:
        # Get file information already in database
        if FileEntity.objects.filter(name=f).count() == 0:
            return "File {} does not exist...quitting".format(f)
        else:
            file_entity = FileEntity.objects.filter(name=f).first()
        latest_history = None
        if file_entity.history.count() != 0:
            latest_history = file_entity.history.latest('inserted')

        # Add new history object if needed
        if latest_history and latest_history.content_hash == data.content_hash:
            return "No updates required"
        new_history = FileHistory(content_hash=data.content_hash,
                                  client_modified=data.client_modified,
                                  server_modified=data.server_modified,
                                  file_entity=file_entity)

        # Non-existent -> Tracked
        # Tracked -> Modified
        if file_entity.status == 'n':
            file_entity.status = 't'
        elif file_entity.status == 't':
            file_entity.status = 'm'

        # Save changes to database
        file_entity.save()
        new_history.save()

        return "Data has been updated"
    else:
        return "File {} does not exist in Dropbox...nothing to update".format(f)

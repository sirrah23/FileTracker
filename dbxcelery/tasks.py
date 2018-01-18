# Basic imports
import sys
import os
import configparser
import django
from celery import Celery
from celery.schedules import crontab

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "filetracker"))
sys.path.insert(0, os.path.dirname(__file__))
# Dropbox
from dbxconn.dbxconn import DBXRepo

# Django models
os.environ['DJANGO_SETTINGS_MODULE'] = 'filetracker.settings'
django.setup()
from tracker.models import FileHistory, FileEntity

# TODO: Move this somewhere else
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

# Celery application
BROKER_URL = 'amqp://{}:{}@localhost:5672/{}'.format(config['Celery']['User'],
                                                     config['Celery']['Password'],
                                                     config['Celery']['VHost'])
app = Celery('tasks', broker=BROKER_URL)

# Dropbox repository object
TOKEN = config['Dropbox']['API_TOKEN']
repo = DBXRepo(TOKEN)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(float(config['Dropbox']['Refresh_Rate']),
                             refresh_file_metadata.s())

@app.task
def refresh_file_metadata():
    """
    Checks all files we are tracking in Dropbox to see if any of them
    have changed and if so, updates them
    """
    print("Starting metadata refresh")
    all_files = FileEntity.objects.all()
    print("Refresh {} files", all_files.count())
    for f in all_files:
        update_file_metadata(f.name)

@app.task
def update_file_metadata(f):
    """
    Given a filename update its modification history based on whether
    or not the file has been updated in Dropbox.
    """
    input_file_set = FileEntity.objects.filter(name=f)
    if input_file_set.count() == 0:
        return {"update": False, "message": "File {} does not exist in system".format(f)}
    file_entity = input_file_set.first()

    dboxdata = repo.get_file_metadata(f)
    if dboxdata:
        # Get file information already in dboxdatabase
        latest_history = None
        if file_entity.history.count() != 0:
            latest_history = file_entity.history.latest('inserted')

        # Create new history object if file has changed
        if latest_history and latest_history.content_hash == dboxdata.content_hash:
            return {"update": False,
                    "message": "File {} has not changed".format(f)}
        new_history = FileHistory(content_hash=dboxdata.content_hash,
                                  client_modified=dboxdata.client_modified,
                                  server_modified=dboxdata.server_modified,
                                  file_entity=file_entity)

        # Pending -> Tracked or
        # Tracked -> Modified
        if file_entity.status == 'p':
            file_entity.status = 't'
        elif file_entity.status == 't':
            file_entity.status = 'm'

        # Save changes to dboxdatabase
        file_entity.save()
        new_history.save()

        return {"update": True, "message": ""}
    else:
        # File Status -> Non-Existent
        file_entity.status = 'n'
        file_entity.save()
        return {"update": "True", "message": "File {} does not exist in Dropbox".format(f)}


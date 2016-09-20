import os
import random
import sys

from ckanapi import RemoteCKAN
import yaml

_DATASETS = []
_CONFIG = {}
_CKAN = None

def load_config(config_file=None):
    global _CONFIG
    loc = config_file or os.environ.get("EMAIL_PUB_CONFIG")
    if not loc:
        print "Need to specify location of config file with EMAIL_PUB_CONFIG"
        sys.exit(1)

    _CONFIG = yaml.load(open(loc, "r").read())

def this_email():
    return _CONFIG.get('from')

def outgoing_mail():
    return _CONFIG.get('smtp')

def incoming_mail():
    return _CONFIG.get('pop3')

def ckan_host():
    return _CONFIG.get('ckan', {}).get('server')

def ckan_apikey():
    return _CONFIG.get('ckan', {}).get('apikey')

def ckan():
    global _CKAN
    if not _CKAN:
        _CKAN = RemoteCKAN(ckan_host(), ckan_apikey())
    return _CKAN

def get_allowed_emails():
    return _CONFIG.get('emails')

def get_users():
    return _CONFIG.get('users')

def get_random_dataset():
    datasets = get_datasets()
    return random.choice(datasets)

def get_datasets():
    from common import random_date
    from datetime import datetime, timedelta

    start = datetime.now()
    end = datetime.now() + timedelta(days=60)

    global _DATASETS

    if not _DATASETS:
        for dataset_name in _CONFIG.get('datasets'):
            dataset = ckan().action.package_show(id=dataset_name)
            due = random_date(start, end )

            dataset["update_due"] = due
            _DATASETS.append(dataset)

    return _DATASETS

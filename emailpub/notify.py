"""
Mimics the process of finding datasets that are due for update.  We don't
currently have an easy mechanism for determining which have upcoming
deadlines, so we'll choose a couple of arbitrary datasets to send to
the user.
"""
import config
import common

def main():
    config.load_config()
    print "Notifying users of upcoming items"

    for user in config.get_users():
        dataset = config.get_random_dataset()

        from common import random_date
        from datetime import datetime, timedelta

        start = datetime.now()
        end = datetime.now() + timedelta(days=60)
        date = random_date(start, end)


        address = common.generate_token_and_address(user, dataset.get('name'), date)
        common.send_notification(user, "data.gov.uk <{}>".format(address), dataset)
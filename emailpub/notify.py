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

    address = common.generate_token_and_address("ross.jones@digital.cabinet-office.gov.uk", "test-dataset")
    common.send_notification("ross.jones@digital.cabinet-office.gov.uk", "data.gov.uk <{}>".format(address))
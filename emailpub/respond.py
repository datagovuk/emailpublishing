import re

import config

from common import generate_schedule, get_latest_messages


def send_schedule(email):
    """ Sends current schedule to the specified user """
    allowed = False
    emails = config.get_allowed_emails()
    for em_re in emails:
        if re.match(em_re, email):
            allowed = True
            break

    if not allowed:
        return

    generate_schedule(email)


def main():
    config.load_config()
    print "Responding to emails"


    # Connect and grab the 10 latest emails
    messages = get_latest_messages()

    # Iterate and process
    for message in messages:
        to = message['Delivered-to']
        frm = message['From']
        if '<' in to:
            email = to[to.index("<")+1:-1]
        else:
            email = frm

        if not '+' in to:
            send_schedule(frm)
            return

        # Find a secret key so we know it is replying to our
        # original notification




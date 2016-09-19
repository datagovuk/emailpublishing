import re

import config

from common import generate_schedule, get_latest_messages, validate_token, raw_email


def email_allowed(email):
    allowed = False
    allowed_emails = config.get_allowed_emails()
    for em_re in allowed_emails:
        if re.match(em_re, email):
            allowed = True
            break

    return allowed

def main():
    config.load_config()
    print "Responding to emails"

    # Connect and grab the 10 latest emails
    messages = get_latest_messages()

    # Iterate and process
    for message in messages:
        print "----"

        to = message['Delivered-to']
        frm = message['From']

        email = raw_email(frm)

        if not email_allowed(email):
            print "{} is not an allowed address".format(email)
            continue

        if not '+' in to:
            print "Generating schedule for {}".format(email)
            #generate_schedule(email)
            continue

        # We need to extract the token from the email address (first+TOKEN@....)
        # and ensure it matches the email address we received.
        first = to[:to.index("@")]
        token = first[first.index("+")+1:]


        print "Looking for token - {}".format(token)
        success, dataset = validate_token(token, frm)
        if not success:
            # Notify user of failure?
            print "FAILED to find a record for the token"
            continue

        print "Looking for URL to add to {}".format(dataset)







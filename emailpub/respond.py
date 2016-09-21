import re

import config

from common import (generate_schedule,
                    get_latest_messages,
                    validate_token,
                    invalidate_token,
                    raw_email,
                    token_from_email)

URL_REGEX = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def email_allowed(email):
    allowed = False
    allowed_emails = config.get_allowed_emails()
    for em_re in allowed_emails:
        if re.match(em_re, email):
            allowed = True
            break

    return allowed

def main(cnf=None):
    config.load_config(cnf)

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
            generate_schedule(email)
            continue

        # We need to extract the token from the email address (first+TOKEN@....)
        # and ensure it matches the email address we received.
        token = token_from_email(to)

        print "Looking for token - {}".format(token)
        success, record = validate_token(token, frm)
        if not success:
            # Notify user of failure?
            print "FAILED to find a record for the token"
            continue

        dataset = record['dataset']
        date = record.get('date')

        print "Looking for URL to add to {}".format(dataset)
        process = None
        payloads = message.get_payload()

        (payload,) = [p for p in payloads if p.get_content_type() == "text/plain"]

        m = [r for r in re.findall(URL_REGEX, payload.as_string()[0:1024])
             if not config.ckan_host() in r]
        if not m:
            print "Could not find any URLs"
            continue

        first_url = m[0]
        print "Processing first URL: {} and adding to {}".format(first_url, dataset)

        """
        print config.ckan().action.resource_create(**{
            'package_id': dataset,
            'url': first_url,
            'description': 'CSV',
            'format': 'CSV',
            'date': date
        })
        invalidate_token(token)
        """



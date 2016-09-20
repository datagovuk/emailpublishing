"""
Generates emails from all of the relevant templates and sends
them to the email address specified on the command line.
"""
import sys

import config
import common
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--to", dest="to",
                  help="Target email address")


def main():
    config.load_config()

    (options, args) = parser.parse_args()

    if not options.to:
        print "Please specify target address with --to my@address.com"
        sys.exit(1)

    print "Generating templates for {}".format(options.to)

    common.send_notification(options.to, config.this_email(), config.get_random_dataset())
    common.generate_schedule(options.to)

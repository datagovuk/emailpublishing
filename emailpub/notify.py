"""
Mimics the process of finding datasets that are due for update.  We don't
currently have an easy mechanism for determining which have upcoming
deadlines, so we'll choose a couple of arbitrary datasets to send to
the user.
"""
import config


def main():
    config.load_config()
    print "Notifying users of upcoming items"


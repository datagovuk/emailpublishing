from datetime import timedelta, datetime
from random import randint
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import poplib
import smtplib

import config

from jinja2 import Environment, PackageLoader


"""
Get the latest n messages from the POP3 server.
"""
def get_latest_messages(n=10):
    messages = []
    settings = config.incoming_mail()

    pop = None
    if settings.get('tls'):
        pp = poplib.POP3_SSL
    else:
        pp = poplib.POP3

    pop = pp(settings.get('host'), settings.get('port'))
    pop.set_debuglevel(1)

    pop.user(settings.get('username'))
    pop.pass_(settings.get('password'))

    fetch_count = n
    (message_count, _) = pop.stat()
    if message_count < n:
        fetch_count = message_count

    for i in range(1, fetch_count+1):
        stat, content_lines, size = pop.top(i, 111000)
        mail = email.message_from_string('\n'.join(content_lines))
        messages.append(mail)

    pop.rset()
    pop.quit()

    return messages


env = Environment(loader=PackageLoader('emailpub', 'templates'))

def generate_schedule(email):
    datasets = config.get_datasets()

    settings = config.outgoing_mail()

    template_html = env.get_template('schedule.html')
    rendered_html = template_html.render(datasets=datasets).encode('utf-8')

    template_text = env.get_template('schedule.txt')
    rendered_text = template_text.render(datasets=datasets)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Publishing Schedule"
    msg['From'] = "publish@data.gov.uk"
    msg['To'] = email

    part1 = MIMEText(rendered_text, 'plain')
    part2 = MIMEText(rendered_html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    sc = None
    if settings.get('tls'):
        sc = smtplib.SMTP_SSL
    else:
        sc = smtplib.SMTP

    print msg

    s = sc(settings.get('host'))
    s.ehlo_or_helo_if_needed()
    s.login(settings.get('username'), settings.get('password'))
    s.sendmail("publish@data.gov.uk", email, msg.as_string())
    s.quit()


def random_date(start, end):
    res = start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))
    return res.strftime("%d/%m/%Y")